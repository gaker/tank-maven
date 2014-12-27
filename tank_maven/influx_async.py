"""
Tornado async wrapper around python-influxdb
"""
import functools
from influxdb import InfluxDBClient as Influx
from tornado import gen, stack_context

from tank_maven.core.conf import settings


def influx_async_coroutine(f):
    """A coroutine that accepts an optional callback.

    Given a callback, the function returns None, and the callback is run
    with (result, error). Without a callback the function returns a Future.
    """
    coro = gen.coroutine(f)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        callback = kwargs.pop('callback', None)
        if callback and not callable(callback):
            raise TypeError("callback must be a callable")
        future = coro(*args, **kwargs)
        if callback:
            def _callback(future):
                try:
                    result = future.result()
                    callback(result, None)
                except Exception as e:
                    callback(None, e)
            future.add_done_callback(_callback)
        else:
            return future
    return wrapper


class InfluxDBClient(Influx):
    """
    Extend
    """
    def __init__(self, **kwargs):
        kwargs['database'] = 'tank_maven'
        super(InfluxDBClient, self).__init__(**kwargs)

    #def query(self, query, time_precision='s', chunked=False, callback=None):
    #    """
#
#        """
#        return super(InfluxDBClient, self).query(
#            query, time_precision=time_precision, chunked=chunked)

