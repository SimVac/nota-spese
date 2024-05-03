import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        client.post(
            '/login',
            data={'username': 'admin', 'password': 'admin'}
        )
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_user_notes(client):
    response = client.get('/user_notes')
    assert response.status_code == 200
    assert ""