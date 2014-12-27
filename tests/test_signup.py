"""
Test login
"""
from .base import TestBase
from tank_maven.models import User


class SignupTest(TestBase):
    """
    Test signup.
    """
    @property
    def url(self):
        return self.reverse_url('sign-up')

    def test_signup_available_with_no_users(self):
        """
        Ensure signup is available if no users are in the DB
        """
        self.assertEqual(0, self.db.query(User).count())

        response = self.get(self.url)
        self.assert200(response)

    def test_user_signup(self):
        """
        Test signing up a user.
        """
        self.assertEqual(
            0, self.db.query(User).count())

        data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': '12345',
            'password_confirm': '12345'
        }
        response = self.post(self.url, data=data)
        self.assert302(response)

        self.assertEqual(
            1, self.db.query(User).count())

    def test_user_exists_and_visits_signup(self):
        """
        Ensure if a user already exists, and they visit signup,
        the page renders a 404
        """
        self.create_user('john', 'john@example.com')
        response = self.get(self.url)
        self.assert404(response)

