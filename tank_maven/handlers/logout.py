
from tank_maven.handlers.base import BaseHandler

class LogoutHandler(BaseHandler):
    """
    Log the user out
    """
    def get(self):
        if not self.get_current_user():
            self.send_error(status_code=404)

        self.clear_cookie('user')
        self.redirect(self.reverse_url('login'))

