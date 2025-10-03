from database import Database
from datetime import datetime

class PatientManager:
    def __init__(self):
        self.db = Database()
    
    def generate_patient_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PAT{timestamp}"
    
    def add_patient(self, name, age, gender, contact=None, address=None, medical_history=None):
        patient_id = self.generate_patient_id()
        
        query = '''
            INSERT INTO patients (patient_id, name, age, gender, contact, address, medical_history)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (patient_id, name, age, gender, contact, address, medical_history)
        
        try:
            self.db.execute_query(query, params)
            return patient_id
        except Exception as e:
            print(f"Error adding patient: {e}")
            return None
    
    def get_patient(self, patient_id):
        query = "SELECT * FROM patients WHERE patient_id = ?"
        return self.db.fetch_one(query, (patient_id,))
    
    def get_all_patients(self):
        query = "SELECT * FROM patients ORDER BY created_at DESC"
        return self.db.fetch_all(query)
    
    def update_patient(self, patient_id, **kwargs):
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE patients SET {set_clause} WHERE patient_id = ?"
        params = tuple(kwargs.values()) + (patient_id,)
        
        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False
    
    def delete_patient(self, patient_id):
        query = "DELETE FROM patients WHERE patient_id = ?"
        try:
            self.db.execute_query(query, (patient_id,))
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
    
    def search_patients(self, search_term):
        query = """
            SELECT * FROM patients 
            WHERE name LIKE ? OR patient_id LIKE ? 
            ORDER BY name
        """
        search_pattern = f"%{search_term}%"
        return self.db.fetch_all(query, (search_pattern, search_pattern))
    
    def schedule_appointment(self, patient_id, appointment_date, doctor_name, department, notes=None):
        query = '''
            INSERT INTO appointments (patient_id, appointment_date, doctor_name, department, notes)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (patient_id, appointment_date, doctor_name, department, notes)
        
        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error scheduling appointment: {e}")
            return False
    
    def get_patient_appointments(self, patient_id):
        query = """
            SELECT * FROM appointments 
            WHERE patient_id = ? 
            ORDER BY appointment_date DESC
        """
        return self.db.fetch_all(query, (patient_id,))
    
    def get_all_appointments(self):
        query = """
            SELECT a.*, p.name as patient_name 
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.patient_id 
            ORDER BY a.appointment_date DESC
        """
        return self.db.fetch_all(query)