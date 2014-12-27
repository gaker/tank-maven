"""
Test login
"""
from .base import TestBase


class LoginTest(TestBase):
    """
    Test login
    """
    @property
    def url(self):
        return self.reverse_url('login')

    def test_no_user_redirects_to_signup(self):
        """
        Ensure that if no users exist when the page is hit the first time,
        the user is redirected to the signup page.
        """
        response = self.get(self.url)
        self.assertRedirects(response, self.reverse_url('sign-up'))

    def test_bad_creds_login_attempt(self):
        """
        Ensure a user gets errors when loggin in with bad creds.
        """
        self.create_user('john', 'john@example.com')

        data = {
            'username': 'john',
            'password': 'b'
        }
        response = self.post(self.url, data=data)
        self.assert200(response)
        self.assertContains(response, 'Invalid username or password')

