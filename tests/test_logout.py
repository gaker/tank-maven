"""
Test logout
"""
from .base import TestBase


class LogoutTest(TestBase):
    """
    Test logout
    """
    @property
    def url(self):
        return self.reverse_url('logout')

    def test_logout_when_not_logged_in(self):
        """
        Ensure a user that is not authenticated gets a 404
        when they hit the logout link
        """
        response = self.get(self.url)
        self.assert404(response)

    def test_logout_with_user(self):
        """
        Ensure a user can log out
        """
        self.create_user('john', 'john@example.com')
        self.login('john')

        response = self.get(self.url)
        self.assertRedirects(response, self.reverse_url('login'))

