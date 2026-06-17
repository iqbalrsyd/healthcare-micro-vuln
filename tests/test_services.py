import requests

BASE_URLS = {
    'auth': 'http://localhost:8001',
    'patient': 'http://localhost:8002',
    'appointment': 'http://localhost:8003',
    'billing': 'http://localhost:8004',
}

def test_health_endpoints():
    for service, url in BASE_URLS.items():
        res = requests.get(f'{url}/health')
        assert res.status_code == 200
        assert res.json()['service'] == service
