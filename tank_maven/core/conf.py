"""
Settings. Liberally borrowed from Django
"""
import importlib
import os


empty_obj = object()


def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty_obj:
            self._setup()
        return func(self._wrapped, *args)
    return inner


class LazySettings(object):

    _wrapped = None

    def __init__(self):
        self._wrapped = empty_obj

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is empty_obj:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError("can't delete _wrapped")
        if self._wrapped is empty_obj:
            self._setup()
        delattr(self._wrapped, name)

    def __getattr__(self, name):
        if self._wrapped is empty_obj:
            self._setup(name)
        return getattr(self._wrapped, name)

    def _setup(self, name=None):
        settings_module = os.environ.get('TANK_MAVEN_SETTINGS')
        if not settings_module:
            raise Exception('TANK_MAVEN_SETTINGS must be set')

        self._wrapped = Settings(settings_module)

    __dir__ = new_method_proxy(dir)


class Settings(object):
    """
    doc
    """
    def __init__(self, settings_module):
        self.SETTINGS_MODULE = settings_module

        module = importlib.import_module(self.SETTINGS_MODULE)

        for setting in dir(module):
            if setting.isupper():
                setting_value = getattr(module, setting)
                setattr(self, setting, setting_value)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


settings = LazySettings()

