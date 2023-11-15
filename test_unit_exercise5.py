import pytest
from exercise4 import app, db, KeyValue, cache

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['CACHE_TYPE'] = 'simple'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_save_and_get(client):
    # Test /save endpoint
    response_save = client.post('/save', json={'key': 'test_key', 'value': 'test_value'})
    assert response_save.status_code == 200

    # Test /get endpoint
    response_get = client.get('/get?key=test_key')
    assert response_get.status_code == 200
    assert response_get.json['key'] == 'test_key'
    assert response_get.json['value'] == 'test_value'

def test_save_invalid_request(client):
    # Test /save with invalid request
    response = client.post('/save', json={'key': 'test_key'})
    assert response.status_code == 400
    assert 'Invalid request' in response.json['error']

def test_get_key_not_found(client):
    # Test /get with key not found
    response = client.get('/get?key=nonexistent_key')
    assert response.status_code == 404
    assert 'Key not found' in response.json['error']

def test_delete(client):
    # Test /save and /delete endpoints
    client.post('/save', json={'key': 'test_key', 'value': 'test_value'})
    
    # Clear the cache
    cache.clear()

    response_delete = client.delete('/delete?key=test_key')
    assert response_delete.status_code == 200

    # Verify that the key is not present after deletion
    response_get = client.get('/get?key=test_key')
    assert response_get.status_code == 404
    assert 'Key not found' in response_get.json['error']


