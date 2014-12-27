
from tank_maven.influx_async import influx_async_coroutine
from tank_maven.handlers.base import LoginRequiredMixin, BaseHandler


class HomeHandler(LoginRequiredMixin, BaseHandler):
    """
    Home page
    """
    template_name = 'home.html'

    @influx_async_coroutine
    def get(self, *args, **kwargs):
        return super(HomeHandler, self).get(*args, **kwargs)

    def _get_temp_data(self):
        """
        Get temp data from influx.
        """
        return self.influx.query('select * from temp')

    def get_context_data(self, **kwargs):
        return super(HomeHandler, self).get_context_data(
            temp_data=self._get_temp_data(),
            **kwargs)

