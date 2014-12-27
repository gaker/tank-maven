"""
Base test class


Parts of this based on:

    https://github.com/peterbe/tornado-utils/blob/master/tornado_utils/http_test_client.py

"""
import Cookie
import unittest
import urllib
from urllib import urlencode
from tornado import escape
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase

from tank_maven.models import User


class TestHttpClient(object):

    def __init__(self, test_base):
        self.get_url = test_base.get_url
        self.http_client = test_base.http_client
        self.wait = test_base.wait
        self.stop = test_base.stop

    def get(self, url, data=None, headers=None, follow_redirects=False):
        """
        Perform a GET request
        """
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, True)
            if '?' in url:
                url += '&%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers=headers,
                           follow_redirects=follow_redirects)

    def post(self, url, data, headers=None, follow_redirects=False):
        """
        perform a POST request.
        """
        if data is not None:
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, unicode):
                        data[key] = value.encode('utf-8')
                data = urlencode(data, True)
        return self._fetch(url, 'POST', data, headers,
                           follow_redirects=follow_redirects)

    def _fetch(self, url, method, data=None, headers=None,
               follow_redirects=True):
        """
        Fetch the URL
        """
        full_url = self.get_url(url)
        request = HTTPRequest(url, follow_redirects=follow_redirects,
                              headers=headers, method=method, body=data)
        self.http_client.fetch(request, self.stop)
        return self.wait()



class TestBase(AsyncHTTPTestCase, LogTrapTestCase):
    """
    Base test class.
    """
    def setUp(self):
        super(TestBase, self).setUp()
        self.application.db.begin(subtransactions=True)
        self.cookies = Cookie.SimpleCookie()
        self.client = TestHttpClient(self)
        self.db = self.application.db

    def tearDown(self):
        super(TestBase, self).tearDown()
        self.application.db.rollback()
        self.application.db.close_all()

    def _render_cookie_back(self):
        return ''.join(['{0}={1}'.format(x, morsel.value)
            for (x, morsel) in self.cookies.items()])

    def _setup_headers(self, headers):
        if self.cookies:
            if headers is None:
                headers = dict()
            headers['Cookie'] = self._render_cookie_back()
        return headers

    def get(self, url, data=None, headers=None, follow_redirects=False):
        """
        perform a GET request
        """
        headers = self._setup_headers(headers)
        response = self.client.get(url, data=data, headers=headers,
                                     follow_redirects=follow_redirects)
        self._update_cookies(response.headers)
        return response

    def post(self, url, data, headers=None, follow_redirects=False):
        """
        Perform a POST request
        """
        headers = self._setup_headers(headers)
        response = self.client.post(url, data=data, headers=headers,
                                      follow_redirects=follow_redirects)
        self._update_cookies(response.headers)
        return response

    def _update_cookies(self, headers):
        try:
            set_cookie = headers['Set-Cookie']
            cookies = escape.native_str(set_cookie)
            self.cookies.update(Cookie.SimpleCookie(cookies))
            while True:
                self.cookies.update(Cookie.SimpleCookie(cookies))
                if ',' not in cookies:
                    break
                cookies = cookies[cookies.find(',') + 1:]
        except KeyError:
            return

    def login(self, username, password='pw'):
        """
        Log the user in.
        """
        data = {
            'username': username,
            'password': password
        }
        url = self.reverse_url('login')
        response = self.post(url, data, follow_redirects=False)
        self.assert302(response)

    def reverse_url(self, name, *args, **kwargs):
        return self.get_url(
            self.application.reverse_url(name, *args, **kwargs))

    @property
    def application(self):
        if not hasattr(self, '_application'):
            setattr(self, '_application', self.get_app())
        return self._application

    def get_app(self):
        from tank_maven.app import application
        return application

    def create_user(self, username, email, password='pw'):
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        self.db.add(user)
        self.db.commit()

        return user

    def get_post_body(self, data):
        return urllib.urlencode(data, doseq=True)

    def assertContains(self, response, item):
        """
        Assert an item is in the response body.
        """
        self.assertTrue(item in response.body)

    def assertRedirects(self, response, url):
        """
        Assert a request redirects
        """
        self.assert302(response)

        location = response.headers.get('Location')
        if url.startswith('http'):
            location = self.get_url(location)
        self.assertEqual(location, url)

    def assert200(self, response):
        self.assertEquals(response.code, 200)
        return response

    def assert302(self, response):
        self.assertEquals(response.code, 302)
        return response

    def assert403(self, response):
        self.assertEquals(response.code, 403)

    def assert404(self, response):
        self.assertEquals(response.code, 404)
        return response

