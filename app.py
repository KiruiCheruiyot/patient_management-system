from flask import Flask, render_template, request, flash, redirect, url_for
from patient_manager import PatientManager

app = Flask(__name__)
app.secret_key = 'patient_management_secret_key_2024'

patient_manager = PatientManager()

@app.route('/')
def index():
    patients = patient_manager.get_all_patients()
    appointments = patient_manager.get_all_appointments()
    
    return render_template('index.html',
                         total_patients=len(patients),
                         total_appointments=len(appointments),
                         recent_patients=patients[:5])

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form.get('contact', '')
        address = request.form.get('address', '')
        medical_history = request.form.get('medical_history', '')
        
        if not name or not age or not gender:
            flash('Please fill in all required fields (Name, Age, Gender).', 'error')
        else:
            patient_id = patient_manager.add_patient(name, age, gender, contact, address, medical_history)
            
            if patient_id:
                flash(f'Patient added successfully! Patient ID: {patient_id}', 'success')
                return redirect(url_for('view_patients'))
            else:
                flash('Error adding patient. Please try again.', 'error')
    
    return render_template('add_patient.html')

@app.route('/view_patients')
def view_patients():
    patients = patient_manager.get_all_patients()
    return render_template('view_patients.html', patients=patients)

@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    results = None
    search_term = ""
    
    if request.method == 'POST':
        search_term = request.form['search_term']
        if search_term:
            results = patient_manager.search_patients(search_term)
    
    return render_template('search_patient.html', results=results, search_term=search_term)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        appointment_date = request.form['appointment_date']
        doctor_name = request.form['doctor_name']
        department = request.form['department']
        notes = request.form.get('notes', '')
        
        # Verify patient exists
        patient = patient_manager.get_patient(patient_id)
        if not patient:
            flash(f'Patient ID {patient_id} does not exist in the system. Please check the Patient ID.', 'error')
        else:
            success = patient_manager.schedule_appointment(patient_id, appointment_date, doctor_name, department, notes)
            if success:
                flash(f'Appointment scheduled successfully for {patient[2]} with Dr. {doctor_name}', 'success')
                return redirect(url_for('appointments'))
            else:
                flash('Error scheduling appointment. Please try again.', 'error')
    
    appointments = patient_manager.get_all_appointments()
    return render_template('appointments.html', appointments=appointments)

if __name__ == '__main__':
    print("🚀 Starting Patient Management System...")
    print("📍 Access the system at: http://localhost:5000")
    print("📍 Or use: http://127.0.0.1:5000")
    print("📍 Press CTRL+C to stop the server")
    print("\n" + "="*50)
    print("✅ System is ready! Open your browser.")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)