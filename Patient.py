from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from database import insert_patient, create_table, get_all_patients, delete_patient_by_id
from database import update_patient

class PatientPage(QWidget):
    patient_deleted = pyqtSignal()

    def __init__(self, dashboard=None):
        super().__init__()
        self.dashboard = dashboard
        self.patient_records = []
        self.init_ui()
        self.resize(1200, 700)
        self.showMaximized()

    def init_ui(self):
        layout = QVBoxLayout(self)
        create_table()

        # Title
        label = QLabel("Patient Data Table")
        label.setFont(QFont("Arial", 20, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        # Count Label
        self.count_label = QLabel()
        self.count_label.setFont(QFont("Arial", 14))
        self.count_label.setAlignment(Qt.AlignCenter)

        # Table
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Contact", "Sex", "DOB", "Address", "Heart Rate", "Status", "Actions"]
        )
        self.table.setColumnHidden(0, True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Load patients
        patients = get_all_patients()
        for patient in patients:
            patient_data = {
                "id": patient[0],
                "name": patient[1],
                "contact": patient[2],
                "sex": patient[3],
                "dob": patient[4],
                "address": patient[5],
                "heart_rate": patient[6],
                "status": patient[7]
            }
            self.patient_records.append(patient_data)
            self.add_patient_to_table(patient_data)

        self.update_count_label()

        # Add Button
        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(self.open_add_patient_dialog)
        add_button.setMinimumWidth(150)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 8px 14px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Layout order
        layout.addWidget(label)
        layout.addWidget(self.count_label)   # <-- new
        layout.addWidget(self.table)
        layout.addWidget(add_button, alignment=Qt.AlignLeft)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background: #f5f6fa; }
            QTableWidget { background: white; border-radius: 5px; font-size: 14px; }
            QHeaderView::section {
                background: #137e8a; color: white; padding: 5px; border: none;
            }
        """)

    def open_add_patient_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Patient")
        form_layout = QFormLayout(dialog)

        name_input = QLineEdit()
        contact_input = QLineEdit()
        sex_input = QLineEdit()
        dob_input = QLineEdit()
        address_input = QLineEdit()
        hr_input = QLineEdit("N/A bpm")
        status_input = QLineEdit()

        form_layout.addRow("Patient Name:", name_input)
        form_layout.addRow("Contact No:", contact_input)
        form_layout.addRow("Sex:", sex_input)
        form_layout.addRow("DOB:", dob_input)
        form_layout.addRow("Address:", address_input)
        form_layout.addRow("Heart Rate:", hr_input)
        form_layout.addRow("Status:", status_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            patient_data = {
                "name": name_input.text(),
                "contact": contact_input.text(),
                "sex": sex_input.text(),
                "dob": dob_input.text(),
                "address": address_input.text(),
                "heart_rate": hr_input.text(),
                "status": status_input.text() or "Normal"
            }

            new_id = insert_patient(**patient_data)
            patient_data["id"] = new_id
            self.patient_records.append(patient_data)
            self.add_patient_to_table(patient_data)
            self.update_count_label()

    def add_patient_to_table(self, patient_data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        columns = ["id", "name", "contact", "sex", "dob", "address", "heart_rate", "status"]
        for col, key in enumerate(columns):
            self.table.setItem(row, col, QTableWidgetItem(str(patient_data[key])))

        delete_button = QPushButton("🗑️")
        delete_button.setStyleSheet("""
            QPushButton { background: transparent; font-size: 16px; }
            QPushButton:hover { background: #b52a37; color: white; }
        """)
        delete_button.clicked.connect(lambda _, r=row: self.delete_patient(r))
        self.table.setCellWidget(row, 8, delete_button)

    def delete_patient(self, row):
        patient = self.patient_records[row]
        patient_id = patient["id"]

        delete_patient_by_id(patient_id)
        self.table.removeRow(row)
        del self.patient_records[row]
        self.update_count_label()

    def update_count_label(self):
        self.count_label.setText(f"Total Patients: {len(self.patient_records)}")
        
    
def save_patient_changes(self):
    update_patient(
        self.selected_id,
        self.name_input.text(),
        self.contact_input.text(),
        self.sex_input.text(),
        self.dob_input.text(),
        self.address_input.text(),
        self.heart_rate_input.text(),
        self.status_input.text()
    )

    # ---- IMPORTANT ----
    # Call Dashboard refresh immediately
    if self.dashboard is not None:
        self.dashboard.update_patient_count()

