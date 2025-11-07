import pytest
from service import app, db
from service.models import Account

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_account(client):
    # Test POST /accounts
    resp = client.post('/accounts', json={
        'name': 'Savings'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == 'Savings'
    assert data['balance'] == 0.0
    assert 'id' in data

def test_get_account_list(client):
    # Create one
    client.post('/accounts', json={'name': 'Checking'})
    # Get list
    resp = client.get('/accounts')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Checking'

def test_get_single_account(client):
    # Create
    post_resp = client.post('/accounts', json={'name': 'Emergency'})
    account_id = post_resp.get_json()['id']
    # Get by ID
    resp = client.get(f'/accounts/{account_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'Emergency'

def test_update_account(client):
    # Create
    post_resp = client.post('/accounts', json={'name': 'Vacation'})
    account_id = post_resp.get_json()['id']
    # Update
    resp = client.put(f'/accounts/{account_id}', json={
        'name': 'Travel Fund',
        'balance': 500.0
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'Travel Fund'
    assert data['balance'] == 500.0

def test_delete_account(client):
    # Create
    post_resp = client.post('/accounts', json={'name': 'Temp'})
    account_id = post_resp.get_json()['id']
    # Delete
    resp = client.delete(f'/accounts/{account_id}')
    assert resp.status_code == 204
    # Confirm gone
    resp = client.get(f'/accounts/{account_id}')
    assert resp.status_code == 404