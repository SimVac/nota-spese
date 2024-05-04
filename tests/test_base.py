from flask_testing import TestCase
import sys
 
sys.path.insert(0, '/home/user/nota-spese/')

from main import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app