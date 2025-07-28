import sqlite3

DB_NAME = "patients.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            sex TEXT,
            dob TEXT,
            address TEXT,
            heart_rate TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_patient(name, contact, sex, dob, address, heart_rate, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, contact, sex, dob, address, heart_rate, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, contact, sex, dob, address, heart_rate, status)
    )
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def get_all_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact, sex, dob, address, heart_rate, status FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return patients

def delete_patient_by_id(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()

def update_patient(id, name, contact, sex, dob, address, heart_rate, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE patients SET name=?, contact=?, sex=?, dob=?, address=?, heart_rate=?, status=? WHERE id=?",
        (name, contact, sex, dob, address, heart_rate, status, id)
    )
    conn.commit()
    conn.close()
