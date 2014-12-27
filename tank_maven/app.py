"""
Tank controller application
"""
import os
import tornado.web
from tornado.ioloop import IOLoop
from tornado.web import Application, url

from tank_maven import uimodules, handlers

if not os.environ.get('TANK_MAVEN_SETTINGS'):
    os.environ['TANK_MAVEN_SETTINGS'] = 'tank_maven.settings.local'

from tank_maven.core.conf import settings


def main():

    from tank_maven.utils import setup_db

    app_settings = {
        'cookie_secret': settings.SECRET_KEY,
        'login_url': '/login/',
        'logout_url': '/logout/',
        'debug': settings.DEBUG,
        'template_path': settings.TEMPLATES_PATH,
        'static_path': settings.STATIC_PATH,
        'ui_modules': uimodules,
    }

    application = Application([
        url(r'/', handlers.HomeHandler, name='home'),
        url(r'^/login/$', handlers.LoginHandler, name='login'),
        url(r'^/logout/$', handlers.LogoutHandler, name='logout'),
        url(r'^/sign-up/$', handlers.SignupHandler, name='sign-up'),
        url(r'^/profile/edit/$', handlers.ProfileEditHandler, name='profile-edit'),
        url(r'^/settings/(.*)/$', handlers.SettingHandler,
            name='setting'),
        url(r'^/settings/$', handlers.SettingsHandler, name='settings-index'),
    ], **app_settings)
    application.db = setup_db()
    return application


application = main()


if __name__ == '__main__':
    application = main()
    application.listen(settings.PORT)
    IOLoop.instance().start()

