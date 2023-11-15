import requests
import pytest
from exercise4 import app, db, KeyValue, cache

@pytest.fixture
def base_url():
    return 'http://localhost:5000'

def test_save_and_get(base_url):
    # Test /save and /get endpoints
    response = requests.post(f'{base_url}/save', json={'key': 'e2e_key', 'value': 'e2e_value'})
    print (response)
    assert response.status_code == 200

    response = requests.get(f'{base_url}/get?key=e2e_key')
    data = response.json()
    assert response.status_code == 200
    assert data['value'] == 'e2e_value'

def test_save_invalid_request(base_url):
    # Test /save endpoint with invalid request
    response = requests.post(f'{base_url}/save', json={'value': 'e2e_value'})
    assert response.status_code == 400

def test_get_missing_key(base_url):
    # Test /get endpoint with missing key
    response = requests.get(f'{base_url}/get')
    assert response.status_code == 400

def test_get_key_not_found(base_url):
    # Test /get endpoint with key not found
    response = requests.get(f'{base_url}/get?key=nonexistent_key')
    assert response.status_code == 404

def test_delete(base_url):
    # Explicitly call /delete to clear the cache after deleting from the database
    response = requests.delete(f'{base_url}/delete?key=e2e_key')
    assert response.status_code == 200

def test_delete_missing_key(base_url):
    # Test /delete endpoint with missing key
    response = requests.delete(f'{base_url}/delete')
    assert response.status_code == 400
