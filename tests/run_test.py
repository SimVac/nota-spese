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
            print(session)
            assert response.status_code == 302
            assert session["logged"] == True


class IndexTest(BaseTestCase):
    def test_index_page(self):
        with self.client as client:
            client.post('/login', data={'username': 'admin', 'password': 'admin'})
            response = client.get('/')
            self.assert200(response)

if __name__ == '__main__':
    unittest.main()