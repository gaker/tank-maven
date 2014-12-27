
from tank_maven import forms
from tank_maven.handlers.base import (
    LoginRequiredMixin, FormMixin, BaseHandler)


class ProfileEditHandler(LoginRequiredMixin, FormMixin, BaseHandler):
    """
    Profile page.
    """
    template_name = 'profile.html'
    form_class = forms.UpdateUserForm

    def get_object(self):
        self.object = self.get_current_user()
        return self.object

    def get_form_kwargs(self, **kwargs):
        return {
            'obj': self.get_object()
        }

