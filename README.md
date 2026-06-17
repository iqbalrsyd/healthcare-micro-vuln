# Healthcare Microservices (Vulnerable)

## Deskripsi

Sistem layanan kesehatan berbasis microservices menggunakan Python + FastAPI. Repository ini **sengaja dibuat rentan** untuk pengujian sistem DevSecOps adaptif terhadap arsitektur microservices dan domain healthcare.

## Ground Truth

| Atribut | Nilai |
|---------|-------|
| Arsitektur | Microservices |
| Domain | Healthcare |
| Bahasa | Python 3.9 |
| Framework | FastAPI |
| Database | PostgreSQL (per service) |
| Deployment | Docker Compose + Kubernetes manifests |
| Tingkat Keamanan | Vulnerable (multi-issue) |

## Struktur Layanan

```text
services/
├── auth/          # Autentikasi & authorization
├── patient/       # Manajemen data pasien (PHI)
├── appointment/   # Janji temu dokter
└── billing/       # Tagihan dan pembayaran
```

## Vulnerability yang Disuntikkan

1. **Hardcoded secrets** — DB credentials dan API keys di source code / config.
2. **Weak inter-service authentication** — service-to-service tanpa token / mTLS.
3. **SQL Injection** — raw query string di beberapa endpoint.
4. **Patient data exposure (PHI leak)** — data pasien terekspos di log dan error response.
5. **Missing input validation** — tidak ada Pydantic schema ketat.
6. **No encryption** — tidak ada TLS enforcement, password plaintext.
7. **Vulnerable dependencies** — `fastapi<0.65.0`, `requests<2.25.0`.
8. **Overly permissive K8s manifests** — privileged container, root user, wide RBAC.
9. **No audit logging** — tidak ada audit trail akses data pasien.
10. **Dockerfile misconfig** — root user, secrets COPY-ed.

## Cara Menjalankan

```bash
docker-compose up --build
```

Service ports:
- Auth: `8001`
- Patient: `8002`
- Appointment: `8003`
- Billing: `8004`

## Endpoint Utama

- `POST /auth/login` — login user
- `GET /patients` — daftar pasien
- `GET /patients/{id}` — detail pasien (PHI)
- `POST /appointments` — buat janji temu
- `POST /billing/invoice` — buat tagihan

## Hasil yang Diharapkan dari Sistem

- **Domain detection:** healthcare
- **Technology detection:** Python, FastAPI, Docker, Kubernetes
- **Architecture detection:** microservices
- **Deployment detection:** Docker + Kubernetes
- **Security needs:** per-service SAST, secret scan, container scan (matrix), API gateway security, service mesh audit, inter-service auth check
- **Risk score:** tinggi
- **Standards coverage:** rendah (HIPAA gap besar)
