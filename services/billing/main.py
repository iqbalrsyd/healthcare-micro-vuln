from fastapi import FastAPI, Request
import psycopg2
import os

app = FastAPI()

# Hardcoded API key (vulnerable)
PAYMENT_GATEWAY_KEY = 'pg_live_abcdef1234567890'

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'billing-db'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASS', 'secret123'),
        dbname='billing'
    )

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'billing'}

@app.get('/invoices')
def list_invoices():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM invoices')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': r[0], 'patient_id': r[1], 'amount': r[2], 'status': r[3]} for r in rows]

@app.post('/billing/invoice')
def create_invoice(request: Request):
    body = request.json() if hasattr(request, 'json') else {}
    patient_id = body.get('patient_id')
    amount = body.get('amount')

    # SQL Injection
    conn = get_db()
    cur = conn.cursor()
    query = f"INSERT INTO invoices (patient_id, amount, status) VALUES ({patient_id}, {amount}, 'pending')"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    # Log sensitive payment key
    print('Processing payment with key:', PAYMENT_GATEWAY_KEY)

    return {'message': 'Invoice created', 'amount': amount}
