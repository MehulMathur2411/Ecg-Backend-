from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QListWidget,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QPushButton,
    QSplitter, QSizePolicy, QGridLayout, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
import numpy as np
import pyqtgraph as pg
from Patient import PatientPage
from database import get_patient_count


# ---------------- Utility Functions ----------------
def generate_base_signals(t):
    """Simulate RA, LA, LL limb electrode signals."""
    heart_rate = 60  # bpm
    freq = heart_rate / 60.0
    ecg_wave = np.sin(2 * np.pi * freq * t) + 0.05 * np.random.randn(len(t))
    RA = ecg_wave + 0.01 * np.random.randn(len(t))
    LA = ecg_wave * 0.9 + 0.01 * np.random.randn(len(t))
    LL = ecg_wave * 1.1 + 0.01 * np.random.randn(len(t))
    return RA, LA, LL

def generate_chest_signals(t):
    """Simulate chest leads (V1-V6)."""
    return [
        1.2*np.sin(2*np.pi*1*t + i*0.2) + 0.01*np.random.randn(len(t))
        for i in range(6)
    ]

def compute_12_leads(RA, LA, LL, V_chest):
    """Compute 12-lead ECG from limb and chest signals."""
    Lead_I = LA - RA
    Lead_II = LL - RA
    Lead_III = LL - LA
    aVR = RA - (LA + LL) / 2
    aVL = LA - (RA + LL) / 2
    aVF = LL - (RA + LA) / 2
    WCT = (RA + LA + LL) / 3
    V_leads = [v - WCT for v in V_chest]
    return [Lead_I, Lead_II, Lead_III, aVR, aVL, aVF] + V_leads


# ---------------- Dashboard Class ----------------
class DashboardWindow(QMainWindow):
    def __init__(self, username="User", switch_to_login_callback=None):
        super().__init__()
        self.switch_to_login_callback = switch_to_login_callback
        self.setWindowTitle("Heart Health Dashboard")
        self.resize(1200, 700)
        self.showMaximized()

        container = QWidget()
        main_layout = QVBoxLayout(container)

        # Header
        header = self.create_header(username)
        main_layout.addWidget(header)

        # Sidebar + Pages
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        self.sidebar = self.create_sidebar()
        splitter.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.home_page(username))
        self.pages.addWidget(self.ecg_page())  # ECG Page
        self.patient_page = PatientPage(dashboard=self)
        self.pages.addWidget(self.patient_page)
        self.pages.addWidget(self.reports_page())
        self.pages.addWidget(self.settings_page())
        splitter.addWidget(self.pages)

        splitter.setSizes([220, 980])
        main_layout.addWidget(splitter)

        self.setCentralWidget(container)
        self.pages.setCurrentIndex(0)

        # Update patient count after everything is loaded
        self.update_patient_count_label()

    # ---------- Header ----------
    def create_header(self, username):
        header_frame = QFrame()
        header_frame.setFixedHeight(70)
        header_frame.setStyleSheet("background-color: white; border-bottom: 1px solid #ccc;")
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(15, 5, 15, 5)

        logo = QLabel()
        pixmap = QPixmap("assets/logo2.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(160, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        else:
            logo.setText("LOGO")
            logo.setFont(QFont("Arial", 18, QFont.Bold))

        title = QLabel("Heart Health Dashboard")
        title.setFont(QFont("Helvetica", 16))
        title.setAlignment(Qt.AlignCenter)

        user_label = QLabel(f"👤 {username}")
        user_label.setFont(QFont("Arial", 14))
        user_label.setAlignment(Qt.AlignVCenter)

        menu_button = QPushButton()
        menu_button.setFixedSize(30, 30)
        menu_button.setStyleSheet(
            "QPushButton { font-size: 18px; border: none; background: transparent; }"
            "QPushButton:hover { background: #f0f0f0; border-radius: 5px; }"
        )

        user_menu = QMenu()
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.handle_logout)
        user_menu.addAction(logout_action)
        menu_button.setMenu(user_menu)

        layout.addWidget(logo)
        layout.addWidget(title, stretch=1)
        layout.addWidget(user_label)
        layout.addWidget(menu_button)
        return header_frame

    # ---------- Sidebar ----------
    def create_sidebar(self):
        sidebar = QListWidget()
        sidebar.addItems(["🏠 Home", "📈 ECG Monitor", "👤 Patient Data", "📑 Reports", "⚙ Settings"])
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px;
            }
            QListWidget::item { height: 40px; padding-left: 10px; }
            QListWidget::item:hover { background: #34495e; border-radius: 5px; }
            QListWidget::item:selected { background: #1abc9c; border-radius: 5px; }
        """)
        sidebar.currentRowChanged.connect(self.switch_page)
        return sidebar

    # ---------- Home Page ----------
    def home_page(self, username):
        page = QWidget()
        layout = QVBoxLayout(page)

        top_frame = QFrame()
        top_frame.setMinimumHeight(80)
        top_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_frame.setStyleSheet("QFrame { background-color: #f5f5f5; border-radius: 10px; padding: 10px; }")
        top_layout = QHBoxLayout(top_frame)
        top_layout.setSpacing(15)

        top_layout.addWidget(self.create_card("❤️ Average Heart Rate", "78 bpm", "#4cb636"))

        patient_card = QFrame()
        patient_card.setStyleSheet("background-color: #78a3c0; color: white; border-radius: 10px; padding: 20px;")
        patient_layout = QVBoxLayout(patient_card)
        patient_label = QLabel("👥 Patients")
        patient_label.setFont(QFont("Arial", 14))
        self.patient_count_label = QLabel("0")
        self.patient_count_label.setFont(QFont("Arial", 24))
        patient_layout.addWidget(patient_label)
        patient_layout.addWidget(self.patient_count_label)
        top_layout.addWidget(patient_card)

        top_layout.addWidget(self.create_card("⚠️ Alerts", 3, "#f12c2c"))

        welcome = QLabel(f"Welcome, {username}! This is your Heart Dashboard")
        welcome.setFont(QFont("Arial", 20))
        welcome.setAlignment(Qt.AlignCenter)

        layout.addWidget(top_frame)
        layout.addWidget(welcome)
        return page

    def update_patient_count_label(self):
        count = get_patient_count()
        self.patient_count_label.setText(str(count))

    def create_card(self, title, value, color="#af3c19"):
        card = QFrame()
        card.setStyleSheet(f"background-color: {color}; color: white; border-radius: 10px; padding: 20px;")
        layout = QVBoxLayout(card)
        label_title = QLabel(title)
        label_title.setFont(QFont("Arial", 14))
        label_value = QLabel(str(value))
        label_value.setFont(QFont("Arial", 24))
        layout.addWidget(label_title)
        layout.addWidget(label_value)
        return card

    # ---------- ECG Page ----------
    def ecg_page(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        label = QLabel("12-Lead ECG Monitor")
        label.setFont(QFont("Arial", 18))
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        grid = QGridLayout()
        main_layout.addLayout(grid)

        self.plots, self.curves, self.data, self.ptrs = [], [], [], []
        for i in range(12):
            plot = pg.PlotWidget(title=f"ECG Lead {i+1}")
            plot.setLabel("bottom", "Time", "s")
            plot.setLabel("left", "Amplitude", "mV")
            plot.showGrid(x=True, y=True)
            curve = plot.plot(pen=pg.intColor(i, hues=12))
            grid.addWidget(plot, i // 3, i % 3)
            self.plots.append(plot)
            self.curves.append(curve)
            self.data.append(np.zeros(200))
            self.ptrs.append(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all_ecg)
        self.timer.start(20)
        return page

    def update_all_ecg(self):
        t = np.linspace(0, 1, 200) + self.ptrs[0] * 0.005
        RA, LA, LL = generate_base_signals(t)
        V_chest = generate_chest_signals(t)
        leads = compute_12_leads(RA, LA, LL, V_chest)

        for i, lead in enumerate(leads):
            self.data[i] = np.roll(self.data[i], -1)
            self.data[i][-1] = lead[-1]
            self.curves[i].setData(self.data[i])

        for i in range(12):
            self.ptrs[i] += 1

    # ---------- Other Pages ----------
    def reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Reports Page")
        label.setFont(QFont("Arial", 18))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    def settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("Settings Page")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)
        return page

    def handle_logout(self):
        if self.switch_to_login_callback:
            self.switch_to_login_callback()
        self.close()

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
