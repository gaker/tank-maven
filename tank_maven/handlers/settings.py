
from tank_maven.handlers.base import LoginRequiredMixin, BaseHandler


class SettingsHandler(LoginRequiredMixin, BaseHandler):
    """
    Handle settings
    """
    template_name = 'settings/index.html'
    valid_settings = {
        'led': 'LED Control'
    }

    def get_context_data(self, **kwargs):
        ctx = super(SettingsHandler, self).get_context_data(**kwargs)
        ctx['valid_settings'] = self.valid_settings
        return ctx


class SettingHandler(SettingsHandler):
    """
    Setup lights
    """
    template_name = 'settings/setting.html'

    def get(self, setting):
        """
        Handle GET
        """
        self.setting_name = setting
        if setting not in self.valid_settings.keys():
            self.send_error(status_code=404)

        return super(SettingHandler, self).get()

    def post(self, setting):
        """
        Handle POST
        """
        pass

    def get_context_data(self, **kwargs):
        """
        Throw ``page_title`` in template context
        """
        ctx = super(SettingHandler, self).get_context_data(**kwargs)
        ctx['page_title'] = self.valid_settings[self.setting_name]
        return ctx

    def get_template(self):
        """
        Figure out which template to use.
        """
        template = super(SettingHandler, self).get_template()
        template_parts = os.path.splitext(template)
        self.template = "{0}-{1}{2}".format(
            template_parts[0], self.setting_name, template_parts[1])
        return self.template

