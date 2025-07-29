import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QHeaderView, QFileDialog, QHBoxLayout,QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from database import insert_patient, create_table, get_all_patients, delete_patient_by_id, update_patient


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

        # --- Buttons Layout ---
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

        export_button = QPushButton("Export Data")
        export_button.setMinimumWidth(150)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 8px 14px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        export_button.clicked.connect(self.export_data_to_excel)

        # Horizontal layout for buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_button)
        btn_layout.addWidget(export_button)

        # Layout order
        layout.addWidget(label)
        layout.addWidget(self.count_label)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # StyleSheet
        self.setStyleSheet("""
            QWidget { background: #f5f6fa; }
            QTableWidget { background: white; border-radius: 5px; font-size: 14px; }
            QHeaderView::section {
                background: #137e8a; color: white; padding: 5px; border: none;
            }
        """)

    def export_data_to_excel(self):
        if not self.patient_records:
            return

        # Convert to DataFrame
        df = pd.DataFrame(self.patient_records)

        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
        if file_path:
            df.to_excel(file_path, index=False)

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
    patient_id = self.selected_patient_id  # Ensure you store selected patient id somewhere
    name = self.name_input.text()
    age = self.age_input.text()
    gender = self.gender_input.currentText()
    contact = self.contact_input.text()

    update_patient(patient_id, name, age, gender, contact)  # Updates DB

    # Update the table in frontend
    self.load_patients()
    QMessageBox.information(self, "Success", "Patient details updated successfully!")
    
