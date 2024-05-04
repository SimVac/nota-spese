from test_base import BaseTestCase

class LoginTest(BaseTestCase):
    def test_get_person_by_id(self):
        response = self.client.post('/login', {
            'admin': 'admin',
            'password': 'password'
        })
        self.assert200(response)