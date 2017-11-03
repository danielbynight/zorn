"""
Zorn main module

This module contains the class definitions which constitute the core of Zorn.
Most of this classes are abstract: they are meant to be extended with the settings
for the Zorn project.
"""
from abc import ABCMeta, abstractmethod


class SettingNotFound(AttributeError):
    """Raise when a setting of a project is not found in its Settings"""
    pass


class Page:
    """Represents a Page in a Zorn project"""
    def __init__(self, template_name, file_name=None, context=None, route='', name=None):
        self.template_name = template_name
        self.file_name = file_name if file_name is not None else template_name.split('/')[-1]
        self.context = context if context else {}
        self.content = ''
        self.route = route
        self.name = name


class Settings(metaclass=ABCMeta):
    """Holds the basic settings for a Zorn project"""
    PAGES = ()
    PROCESSORS = ()
    PLUGINS = ()

    @property
    @abstractmethod
    # pylint: disable=invalid-name
    def ROOT_DIR(self):
        pass

    @property
    @abstractmethod
    # pylint: disable=invalid-name
    def TEMPLATES_DIR(self):
        pass


class SettingsMixin(metaclass=ABCMeta):
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, setting):
        try:
            return getattr(self.settings, setting)
        except AttributeError:
            raise SettingNotFound(
                '{setting} has to be be defined in the project settings in order to use {class_name}'
                .format(setting=setting, class_name=self.__class__.__name__)
            )


class Project(SettingsMixin):
    def generate(self):
        for plugin in self.settings.PLUGINS:
            plugin(self.settings).run()

        processors = [processor(self.settings) for processor in self.settings.PROCESSORS]

        for page in self.settings.PAGES:
            for processor in processors:
                processor.render(page)


class Processor(SettingsMixin, metaclass=ABCMeta):
    @abstractmethod
    def render(self, page):
        pass


class Plugin(SettingsMixin, metaclass=ABCMeta):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
