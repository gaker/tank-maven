"""
Test login
"""
import urllib
from .base import TestBase
from tank_maven.models import User


class SignupTest(TestBase):
    """
    Test signup.
    """
    @property
    def url(self):
        return self.reverse_url('profile-edit')

    @property
    def user(self):
        return self.create_user('john', 'john@example.com')

#    def test_logged_out(self):
#        """
#        Ensure a logged out user can't access
#        """
#        redirect_url = '{0}?{1}'.format(
#            self.reverse_url('login'),
#            urllib.urlencode({'next': '/profile/edit/'}))
#
#        response = self.get(self.url)
#        self.assertRedirects(response, redirect_url)
#
#        response = self.post(self.url, data={})
#        self.assert403(response)
#
    #def test_logged_in(self):
    #    """
    #    Ensure a logged in user can access
    #    """
    #    self.login('john')
#
#        response = self.get(self.url)
#        self.assert200(response)
#        self.assertIn('john@example.com', response.body)

    #def test_change_data(self):
    #    """
    #    Ensure a users profile data can be changed.
    #    """
    #    self.login(self.user.username)
    #    data = {
    #        'username': self.user.username,
    #        'email': 'john1@example.com'
    #    }
    #    response = self.post(self.url, data=data)
    #    self.assert302(response)

        #user = self.db.query(User).filter(User.id == self.user.id).first()

        #self.assertEquals(user.email, data.get('email'))
        #self.assertEquals(user.username, data.get('username'))

