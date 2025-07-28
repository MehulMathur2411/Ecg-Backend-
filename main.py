import sys
import json
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QStackedWidget,QFormLayout,QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap,  QColor
from dash import DashboardWindow
from Patient import PatientPage
from database import insert_patient, create_table


AUTH_FILE = os.path.join(os.path.dirname(__file__), "auth_data.json")


# --- Load users ---
def load_users():
    if not os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'w') as f:
            json.dump({}, f)
    with open(AUTH_FILE, 'r') as f:
        data = json.load(f)
        print("Loaded Users:", data)  # <-- Add this
        return data


# --- Save users ---
def save_users(users):
    with open(AUTH_FILE, 'w') as f:
        json.dump(users, f, indent=4)
        f.flush()
        os.fsync(f.fileno())


def save_users(users):
    print("Saved:", users)

class SignUpWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setFixedSize(450, 400)
        self.setStyleSheet("background-color: #9ECAD6;")

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Card-like container
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(40, 30, 40, 30)
        container.setLayout(container_layout)
        container.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        container.setGraphicsEffect(shadow)

        # Heading
        title_label = QLabel("Create an Account")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # --- Form Layout ---
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        form_layout.setAlignment(Qt.AlignCenter)

        def add_form_row(label_text, widget):
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 11))
            label.setFixedWidth(100)  # Equal label width
            widget.setFixedWidth(200)  # Equal input width
            row.addWidget(label)
            row.addWidget(widget)
            row.setAlignment(Qt.AlignCenter)
            form_layout.addLayout(row)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")

        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("Enter mobile number")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter user ID")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)

        add_form_row("Username:", self.username_input)
        add_form_row("Full Name:", self.name_input)
        add_form_row("Mobile:", self.mobile_input)
        add_form_row("User ID:", self.id_input)
        add_form_row("Password:", self.password_input)

        container_layout.addLayout(form_layout)

        # --- Buttons ---
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7; 
                color: white; 
                padding: 8px; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        signup_button.clicked.connect(self.signup)

        login_switch_button = QPushButton("Already have an account? Sign In")
        login_switch_button.setStyleSheet("""
            QPushButton {
                color: #0078d7; 
                background: none; 
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        login_switch_button.clicked.connect(switch_to_login)

        container_layout.addWidget(signup_button)
        container_layout.addWidget(login_switch_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        user_id = self.id_input.text().strip()

        # Basic validation
        if not username or not password or not name or not mobile or not user_id:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        # Mobile number validation
        if not re.match(r'^[6-9]\d{9}$', mobile):
            QMessageBox.warning(self, "Invalid Mobile", "Mobile number must be 10 digits and start with 6, 7, 8, or 9")
            return

        users = load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username already exists!")
            return

        users[username] = {"password": password, "name": name, "mobile": mobile, "id": user_id}
        save_users(users)

        QMessageBox.information(self, "Success", "Account created! Please sign in.")
        self.username_input.clear()
        self.name_input.clear()
        self.mobile_input.clear()
        self.id_input.clear()
        self.password_input.clear()



# --- Sign In Page ---
class SignInWindow(QWidget):
    def __init__(self, switch_to_signup, switch_to_dashboard):
        super().__init__()
        self.switch_to_dashboard = switch_to_dashboard
        self.setStyleSheet("background-color: #f0f0f0;")
        main_layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(150, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Welcome label
        label = QLabel("DeckMount Welcomes You!")
        label.setAlignment(Qt.AlignHCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(32)
        label.setFont(font)
        label.setStyleSheet("font-weight: bold; color: blue;")
        main_layout.addWidget(label)

        # Form
        form_frame = QFrame()
        form_frame.setFixedWidth(300)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #007acc;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Sign In")
        login_button.clicked.connect(self.signin)

        signup_button = QPushButton("Don't have an account? Sign Up")
        signup_button.clicked.connect(switch_to_signup)

        for w in (self.username_input, self.password_input, login_button, signup_button):
            form_layout.addWidget(w)
        form_frame.setLayout(form_layout)

        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_frame)
        main_layout.addLayout(form_wrapper)

        self.setLayout(main_layout)

    def signin(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        users = load_users()
        if username in users and users[username]["password"] == password:
            self.switch_to_dashboard(username)
        else:
            QMessageBox.warning(self, "Failed", "Invalid username or password")

# --- Main Window with QStackedWidget ---
class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.signin_page = SignInWindow(self.switch_to_signup, self.switch_to_dashboard)
        self.signup_page = SignUpWindow(self.show_login)
        self.addWidget(self.signin_page)
        self.addWidget(self.signup_page)
        self.setCurrentWidget(self.signin_page)

    def switch_to_dashboard(self, username):
        self.dashboard_page = DashboardWindow(username, self.show_login)
        self.addWidget(self.dashboard_page)
        self.setCurrentWidget(self.dashboard_page)

    def switch_to_signup(self):
        self.setCurrentWidget(self.signup_page)

    def show_login(self):
        self.setCurrentWidget(self.signin_page)

# --- Database Table Create ---
create_table()

# --- Run Application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1200, 700)
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())
