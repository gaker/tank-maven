
import tornado
from tornado.web import RequestHandler
from tank_maven import models
from tank_maven.core.conf import settings
from tank_maven.influx_async import InfluxDBClient


class TemplateMixin(object):
    """
    Mixin that handles rendering a template for GET requests.
    """
    template_name = None

    def get_template(self):
        if self.template_name is None:
            raise Exception('A template name is required')
        return self.template_name

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self):
        return self.render(self.get_template(), **self.get_context_data())


class FormMixin(object):
    """
    A mixin that handles form processing.
    """
    form_class = None

    def get_form(self):
        if self.form_class is None:
            raise Exception('A form class is required')
        return self.form_class

    def get_form_kwargs(self, **kwargs):
        return kwargs

    def get_success_url(self):
        """
        Get a "success" URL to redirect to after a successful form
        submission
        """
        return self.request.full_url()

    def get(self):
        """
        Handle a GET request
        """
        form_class = self.get_form()
        form = form_class(**self.get_form_kwargs())
        self.render(self.get_template(), **self.get_context_data(form=form))

    def post(self):
        """
        Handle a POST request
        """
        form_class = self.get_form()
        form = form_class(self.request.arguments, **self.get_form_kwargs())

        if form.validate():
            return self.save(form)

        self.render(self.get_template(), **self.get_context_data(form=form))

    def save(self, form):
        """
        Save an object.
        """
        # @todo -- is this the right way to do it?
        if self.object:
            for k, v in form.data.items():
                if hasattr(self.object, k):
                    setattr(self.object, k, v)

            self.db.add(self.object)
            self.db.commit()
            return self.redirect(self.get_success_url())

        return None


class BaseHandler(TemplateMixin, RequestHandler):
    """
    Base handler
    """
    @property
    def db(self):
        """
        Sets up the database.

        If the environment variable ``TANK_MAVEN_TEST`` is set,
        an in-memory SQLite database is used.
        """
        return self.application.db

    @property
    def influx(self):
        """
        Sets up an influx DB connection
        """
        if not hasattr(self, '_influx_client'):
            opts = {
                'username': settings.INFLUX.get('username'),
                'password': settings.INFLUX.get('password'),
                'database': settings.INFLUX.get('database'),
            }

            self._influx_client = InfluxDBClient(**opts)
        return self._influx_client

    def get_current_user(self):
        """
        Return the current user
        """
        user_id = self.get_secure_cookie('user')
        if not user_id:
            return None
        return self.db.query(models.User).get(user_id)

    def get_logout_url(self):
        """
        Logout URL
        """
        return self.application.settings["logout_url"]

    def get_form_kwargs(self, **kwargs):
        """
        Get keyword arguments to pass to the form class
        """
        return kwargs

    def get_form(self):
        """
        Get the form class
        """
        return self.form_class


class LoginRequiredMixin(object):
    """
    A mixin that requires a user to be logged in
    """
    @tornado.web.authenticated
    def prepare(self):
        return super(LoginRequiredMixin, self).prepare()

