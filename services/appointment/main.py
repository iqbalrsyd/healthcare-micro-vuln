from fastapi import FastAPI, Request
import psycopg2
import requests
import os

app = FastAPI()

AUTH_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth:8000')

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'appointment-db'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASS', 'secret123'),
        dbname='appointment'
    )

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'appointment'}

@app.get('/appointments')
def list_appointments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM appointments')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': r[0], 'patient_id': r[1], 'doctor': r[2], 'time': r[3]} for r in rows]

@app.post('/appointments')
def create_appointment(request: Request):
    body = request.json() if hasattr(request, 'json') else {}
    patient_id = body.get('patient_id')
    doctor = body.get('doctor')
    time = body.get('time')

    # Weak auth check: only verifies token presence, not signature sometimes
    token = body.get('token')
    if not token:
        return {'error': 'Missing token'}, 401

    conn = get_db()
    cur = conn.cursor()
    query = f"INSERT INTO appointments (patient_id, doctor, appointment_time) VALUES ({patient_id}, '{doctor}', '{time}')"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return {'message': 'Appointment created'}
