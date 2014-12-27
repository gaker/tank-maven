"""
UIModules
"""

import logging
from tornado.web import UIModule


gen_log = logging.getLogger("tornado.application")


class FormModule(UIModule):
    """
    render form fields.
    """
    def render(self, field=None):
        """
        Render the field in a bootstrap way.
        """
        fields = ('TextField', 'PasswordField')
        result = ''

        if field.type in fields:
            context = {
                'label': field.label(class_=' control-label'),
                'field': field(
                    class_='form-control',
                    placeholder=field.label.text),
                'errors': field.errors or ''
            }
            result = self.render_string('forms/input.html', **context)

        return result


class SideNavItem(UIModule):
    """
    Determines if the nav is active or not
    """
    def is_current(self, url):
        """
        determine if the requested URL is the current URL
        """
        return self.request.uri == url

    def render(self, url_name, url_arg, title):
        """
        Render the nav item
        """
        try:
            url = self.handler.reverse_url(url_name, url_arg)
        except KeyError:
            gen_log.warn('Invalid reverse url {0}'.format(url_name))
            return ''

        context = {
            'url': url,
            'is_current': self.is_current(url),
            'title': title
        }
        return self.render_string('includes/side_nav_item.html', **context)

