import re
import unittest
from flask import url_for
from app import db, create_app
from models import User
import client
from flask import current_app


class FlaskClientTestCase(unittest.TestCase):
    client = client

    def setUp(self):
        """Set up application for testing."""
        with self.test_app.app_context():
            self.test_app = current_app.test_client()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_register_and_login(self):
        # register a new account
        response = self.app.post(url_for('auth.register'), data={
            'name': 'john',
            'location': 'dainville',
            'email': 'john@example.com',
            'password': 'cats1234'
        })
        self.assertTrue(response.status_code == 302)
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\s+john!', data))
        self.assertTrue('You have not confirmed your account yet' in data)
        # send a confirmation token
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)
        # log out
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
