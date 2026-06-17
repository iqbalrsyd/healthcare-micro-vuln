from fastapi import FastAPI, Request
import psycopg2
import jwt
import os

app = FastAPI()

# Hardcoded secret (vulnerable)
JWT_SECRET = os.getenv('JWT_SECRET', 'weakjwtsecret')
DB_PASS = os.getenv('DB_PASS', 'secret123')

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'auth-db'),
        user=os.getenv('DB_USER', 'admin'),
        password=DB_PASS,
        dbname='auth'
    )

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'auth'}

@app.post('/auth/login')
def login(request: Request):
    body = request.json() if hasattr(request, 'json') else {}
    email = body.get('email')
    password = body.get('password')

    # SQL Injection vulnerable
    conn = get_db()
    cur = conn.cursor()
    query = f"SELECT id, role FROM users WHERE email = '{email}' AND password = '{password}'"
    cur.execute(query)
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return {'error': 'Invalid credentials'}, 401

    token = jwt.encode({'id': user[0], 'role': user[1]}, JWT_SECRET, algorithm='HS256')
    return {'token': token}

@app.get('/auth/verify')
def verify(token: str):
    # No signature verification in some paths (vulnerable)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except Exception:
        return {'error': 'Invalid token'}, 401
