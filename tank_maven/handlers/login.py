
from bcrypt import hashpw, gensalt
from tank_maven import forms, models
from tank_maven.handlers.base import FormMixin, BaseHandler


class LoginHandler(FormMixin, BaseHandler):
    """
    Login page
    """
    form_class = forms.LoginForm
    template_name = 'login.html'

    def prepare(self):
        """
        Check to see if a user exists in the database,
        if there is not on, redirect to the signup page.
        """
        if self.db.query(models.User).count() == 0:
            return self.redirect(self.reverse_url('sign-up'))

    def save(self, form):
        """
        Handle POST
        """
        username = self.get_argument('username')
        password = self.get_argument('password').encode('utf-8')

        user = self.db.query(models.User).filter(models.User.id == 1).first()

        if user:
            hashed_pw = user.password.encode('utf-8')
            valid = hashpw(password, hashed_pw) == hashed_pw
            if valid:
                self.set_secure_cookie('user', str(user.id))
                return self.redirect(self.reverse_url('home'))

        form.username.errors.append(u'Invalid username or password')
        return self.render('login.html', form=form)

