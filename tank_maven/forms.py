"""
Forms
"""
from wtforms import TextField, PasswordField, validators
from wtforms_tornado import Form


class FormPasswordMixin(object):
    """
    Form password Mixin

    Adds ``password`` & ``password_confirm`` fields
    """
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=5),
        validators.EqualTo(
            'password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Password Repeated')


class LoginForm(Form):
    """
    Login form.
    """
    username = TextField('Username', [
        validators.Length(min=4)])
    password = PasswordField('Password',
        [validators.InputRequired()])


class SignupForm(Form, FormPasswordMixin):
    """
    Signup form.
    """
    username = TextField('Username', [
        validators.Length(min=4, max=30),
        validators.InputRequired()])
    email = TextField('Email', [
        validators.Length(max=255),
        validators.InputRequired(),
        validators.Email()])


class UpdateUserForm(Form):
    """
    Update user form
    """
    username = TextField('Username', [
        validators.Length(min=4, max=30),
        validators.InputRequired()])
    email = TextField('Email', [
        validators.Length(max=255),
        validators.InputRequired(),
        validators.Email()])


class ChangePasswordForm(Form, FormPasswordMixin):
    """
    Change a users password
    """

