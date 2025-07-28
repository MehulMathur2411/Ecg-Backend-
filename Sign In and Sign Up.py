import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QStackedLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

AUTH_FILE = "auth_data.json"

def load_users():
    if not os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'w') as f:
            json.dump({}, f)
    with open(AUTH_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(AUTH_FILE, 'w') as f:
        json.dump(users, f, indent=4)

class SignUpForm(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Create Your Account")
        label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")

        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("Mobile Number")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("User ID")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.signup)

        switch_btn = QPushButton("Already have an account? Sign In")
        switch_btn.clicked.connect(switch_to_login)

        for w in [self.username_input, self.name_input, self.mobile_input, self.id_input, self.password_input, signup_btn, switch_btn]:
            w.setStyleSheet("""
                QLineEdit, QPushButton {
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #007acc;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #005f99;
                }
            """)
            layout.addWidget(w)
        layout.insertWidget(0, label)

        self.setLayout(layout)

    def signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        user_id = self.id_input.text().strip()

        if not all([username, password, name, mobile, user_id]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        users = load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username already exists.")
            return

        users[username] = {
            "password": password,
            "name": name,
            "mobile": mobile,
            "id": user_id
        }
        save_users(users)

        QMessageBox.information(self, "Success", "Account created successfully.")
        self.username_input.clear()
        self.password_input.clear()
        self.name_input.clear()
        self.mobile_input.clear()
        self.id_input.clear()

class SignInForm(QWidget):
    def __init__(self, switch_to_signup):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Welcome Back!")
        label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Sign In")
        login_btn.clicked.connect(self.signin)

        switch_btn = QPushButton("Don't have an account? Sign Up")
        switch_btn.clicked.connect(switch_to_signup)

        for w in [self.username_input, self.password_input, login_btn, switch_btn]:
            w.setStyleSheet("""
                QLineEdit, QPushButton {
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #28a745;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            layout.addWidget(w)
        layout.insertWidget(0, label)

        self.setLayout(layout)

    def signin(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        users = load_users()

        if username in users and users[username]["password"] == password:
            name = users[username]["name"]
            QMessageBox.information(self, "Success", f"Welcome {name}!")
        else:
            QMessageBox.warning(self, "Failed", "Invalid credentials.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeckMount Login Portal")
        self.setMinimumSize(1000, 600)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 14px;
            }
        """)

        main_layout = QHBoxLayout(self)

        # === Left Panel (Branding) ===
        branding_frame = QFrame()
        branding_layout = QVBoxLayout()
        branding_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #007acc, stop:1 #005f99);
                color: white;
            }
        """)
        branding_frame.setFixedWidth(400)

        logo = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(200, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("DeckMount\nHealth Portal")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")

        branding_layout.addStretch()
        branding_layout.addWidget(logo)
        branding_layout.addWidget(title)
        branding_layout.addStretch()
        branding_frame.setLayout(branding_layout)

        # === Right Panel with Forms ===
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #f7f7f7;")
        right_layout = QVBoxLayout()

        # Card container
        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ccc;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
            }
        """)
        form_card.setFixedWidth(420)

        self.stack = QStackedLayout()
        self.signin_form = SignInForm(self.show_signup)
        self.signup_form = SignUpForm(self.show_signin)
        self.stack.addWidget(self.signin_form)
        self.stack.addWidget(self.signup_form)
        form_card.setLayout(self.stack)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_card)
        center_layout.addStretch()

        right_layout.addStretch()
        right_layout.addLayout(center_layout)
        right_layout.addStretch()
        right_panel.setLayout(right_layout)

        main_layout.addWidget(branding_frame)
        main_layout.addWidget(right_panel)

        self.show_signin()

    def show_signin(self):
        self.stack.setCurrentWidget(self.signin_form)

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_form)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
