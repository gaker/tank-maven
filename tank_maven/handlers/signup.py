
from tank_maven import forms, models
from tank_maven.handlers.base import FormMixin, BaseHandler


class SignupHandler(FormMixin, BaseHandler):
    """
    Signup page.
    """
    form_class = forms.SignupForm
    template_name = 'sign-up.html'

    def prepare(self):
        """
        Throw a 404 if there is more than 0 users in the database.
        """
        if self.db.query(models.User).count() != 0:
            self.send_error(status_code=404)

    def save(self, form):
        """
        save the form
        """
        user = models.User()
        user.username = self.get_argument('username')
        user.email = self.get_argument('email')
        user.set_password(self.get_argument('password').encode('utf-8'))

        self.db.add(user)
        self.db.commit()

        self.set_secure_cookie('user', str(user.id))
        self.redirect(self.reverse_url('home'))

