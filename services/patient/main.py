from fastapi import FastAPI, Request
import psycopg2
import requests
import os

app = FastAPI()

AUTH_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth:8000')

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'patient-db'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASS', 'secret123'),
        dbname='patient'
    )

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'patient'}

@app.get('/patients')
def list_patients():
    # No authentication check
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, name, date_of_birth, ssn, medical_history FROM patients')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # PHI logged to console (vulnerable)
    print('Fetched patients:', rows)

    return [{'id': r[0], 'name': r[1], 'dob': r[2], 'ssn': r[3], 'history': r[4]} for r in rows]

@app.get('/patients/{patient_id}')
def get_patient(patient_id: int):
    # SQL Injection possible via string concatenation
    conn = get_db()
    cur = conn.cursor()
    query = f"SELECT * FROM patients WHERE id = {patient_id}"
    cur.execute(query)
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        # Verbose error leaks DB info
        return {'error': f'Patient with id {patient_id} not found in patients table'}, 404

    return {'id': row[0], 'name': row[1], 'dob': row[2], 'ssn': row[3], 'history': row[4]}

@app.post('/patients')
def create_patient(request: Request):
    body = request.json() if hasattr(request, 'json') else {}
    name = body.get('name')
    dob = body.get('date_of_birth')
    ssn = body.get('ssn')

    # No input validation, no encryption
    conn = get_db()
    cur = conn.cursor()
    query = f"INSERT INTO patients (name, date_of_birth, ssn) VALUES ('{name}', '{dob}', '{ssn}')"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return {'message': 'Patient created'}
