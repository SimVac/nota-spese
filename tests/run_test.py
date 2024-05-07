import unittest
from flask import session
import test_index
from test_base import BaseTestCase

class LoginTest(BaseTestCase):
    def test_login_page(self):
        with self.client as client:
            response = client.get('/login')
            self.assert200(response)

    def test_login(self):
        with self.client as client:
            response = client.post('/login', data={'username': 'admin', 'password': 'admin'})
            assert response.status_code == 302
            assert session["logged"] == True

    def test_logout(self):
        with self.client as client:
            response = client.get("/logout")
            assert response.status_code == 302


class IndexTest(BaseTestCase):
    def test_index_page(self):
        with self.client as client:
            client.post('/login', data={'username': 'test', 'password': 'test'})
            response = client.get('/')
            assert response.status_code == 302


class AddNotaTest(BaseTestCase):
    def test_add_nota_route(self):
        with self.client as client:
            client.post('/login', data={'username': 'admin', 'password': 'admin'})
            response = client.get('/add-nota')
            assert response.status_code == 200


class ApiTest(BaseTestCase):
    def test_api_get_note(self):
        with self.client as client:
            client.post('/login', data={'username': 'admin', 'password': 'admin'})
            response = client.get('/api/user-notes/1')
            assert response.status_code == 200




if __name__ == '__main__':
    unittest.main()