import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QListWidget,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame,
    QPushButton, QMessageBox, QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DashboardWindow(QMainWindow):
    def __init__(self, username="User", switch_to_login_callback=None):
        super().__init__()
        self.username = username
        self.last_login_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.switch_to_login_callback = switch_to_login_callback

        self.setWindowTitle(" Deck Mount ECG Monitor")
        self.resize(1200, 700)
        self.setStyleSheet("font-family: 'Segoe UI';")

        container = QWidget()
        container.setStyleSheet("background-color: aliceblue;")
        main_layout = QHBoxLayout(container)

        
        self.sidebar = QListWidget()
        self.sidebar.addItems(["\U0001F3E0 Home", "\U0001F4C4 Reports", "\U0001F512 Logout"])
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: lightsteelblue;
                color: navy;
                font-size: 17px;
                border: none;
                padding: 10px;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
            QListWidget::item {
                height: 45px;
                padding-left: 18px;
                margin-bottom: 6px;
            }
            QListWidget::item:hover {
                background: skyblue;
                border-radius: 10px;
            }
            QListWidget::item:selected {
                background: deepskyblue;
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
        """)
        self.sidebar.currentRowChanged.connect(self.switch_page)

       
        self.pages = QStackedWidget()
        self.pages.addWidget(self.home_page())
        self.pages.addWidget(self.reports_page())

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)
        self.setCentralWidget(container)
        self.pages.setCurrentIndex(0)

    def home_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: aliceblue;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("\U0001F4CA Deck Mount ECG Dashboard")
        title.setFont(QFont("Times New Roman", 28, QFont.Bold))
        title.setStyleSheet("color: navy;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        layout.addSpacing(30)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: lightcyan;
                border-radius: 18px;
                padding: 35px;
                border: 1px solid lightsteelblue;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)

        greeting = QLabel(f" Welcome, {self.username}")
        greeting.setFont(QFont("Times New Roman", 22, QFont.Bold))
        greeting.setStyleSheet("color: navy;")

        login_info = QLabel(f" Last Login: {self.last_login_time}")
        login_info.setFont(QFont("Segoe UI", 16))
        login_info.setStyleSheet("color: darkgreen;")

        subtext = QLabel(
            "Use the navigation menu to view your reports,\n"
            "or securely log out of your ECG Dashboard."
        )
        subtext.setFont(QFont("Times New Roman", 18))
        subtext.setStyleSheet("color: darkslategray;")
        subtext.setWordWrap(True)

        card_layout.addWidget(greeting)
        card_layout.addWidget(login_info)
        card_layout.addSpacing(15)
        card_layout.addWidget(subtext)

        layout.addWidget(card)

        return page

    def reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 30, 50, 30)

        title = QLabel("\U0001F4C4 ECG Report Summary")
        title.setFont(QFont("Georgia", 22, QFont.Bold))
        title.setStyleSheet("color: navy;")
        title.setAlignment(Qt.AlignCenter)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by patient name...")
        self.search_bar.setFixedHeight(35)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 6px 12px;
                border-radius: 10px;
                border: 2px solid lightblue;
            }
        """)
        self.search_bar.textChanged.connect(self.update_report_list)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.search_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_container = QWidget()
        self.report_layout = QVBoxLayout(self.scroll_container)

        self.reports = [
            {"name": "abc", "age": 52, "date": "28-07-2025", "rate": 76, "rhythm": "Normal", "comments": "No abnormalities detected."},
            {"name": "xyz", "age": 34, "date": "26-07-2025", "rate": 88, "rhythm": "Mild abnormality found", "comments": "Mild elevation in heart rate."},
            {"name": "stu", "age": 60, "date": "25-07-2025", "rate": 65, "rhythm": "Normal", "comments": "Healthy ECG."},
            {"name": "ftr", "age": 46, "date": "22-07-2025", "rate": 72, "rhythm": "Normal", "comments": "No concern detected."}
        ]

        self.scroll.setWidget(self.scroll_container)
        layout.addWidget(self.scroll)

        self.update_report_list()

        return page

    def update_report_list(self):
        for i in reversed(range(self.report_layout.count())):
            widget = self.report_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        keyword = self.search_bar.text().strip().lower()
        filtered = [r for r in self.reports if keyword in r["name"].lower()]

        for report in filtered:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    padding: 20px;
                    border: 2px solid #ADD8E6;
                }
            """)
            frame_layout = QVBoxLayout(frame)
            report_text = QLabel(f"""
            <b> Patient:</b> {report['name']} &nbsp;&nbsp; <b>Age:</b> {report['age']} <br>
            <b> Date:</b> {report['date']}<br>
            <b> Heart Rate:</b> {report['rate']} bpm<br>
            <b> Rhythm:</b> {report['rhythm']}<br>
            <b> Comments:</b> {report['comments']}
            """)
            report_text.setTextFormat(Qt.RichText)
            report_text.setFont(QFont("Segoe UI", 14))
            frame_layout.addWidget(report_text)
            self.report_layout.addWidget(frame)
            self.report_layout.addSpacing(10)

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.switch_to_login_callback:
                self.switch_to_login_callback()
            self.close()

    def switch_page(self, index):
        if index == 2:
            self.handle_logout()
        else:
            self.pages.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow("XYZ")
    window.show()
    sys.exit(app.exec_())
