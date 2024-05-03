import pytest
from ..main import app



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_login_route(client):
    response = client.get('/login')
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert '<form method="post">' in data
    assert '<input type="text" class="grow" placeholder="Username" name="username"/>' in data
    assert '<input type="password" class="grow" placeholder="Password" name="password"/>' in data
    assert '<button class="btn" type="submit">Entra</button>' in data


def test_get_user_notes(client):
    response = client.post('/login', {
        'username': 'admin',
        'password': 'admin'
    })
    assert response.status_code == 200
    assert 'session' in response.cookies