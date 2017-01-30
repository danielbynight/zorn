class ZornError(Exception):
    """Base class for general Zorn exceptions"""
    pass


class NotAZornProjectError(ZornError):
    """Indicates that the 'zorn' command was used while in a directory which doesn't contain a Zorn project"""
    pass


class PageError(ZornError):
    """General error for exceptions related with pages"""
    pass


class PathNotFound(PageError):
    """Indicates that the given path doesn't correspond to any page"""
    pass


class SettingsError(ZornError):
    """General error for exceptions related with settings"""
    pass


class SettingNotFoundError(SettingsError):
    """Indicates that a non-optional settings wasn't passed to the object"""
    pass


class UnknownStyleError(SettingsError):
    """Indicates that a non-registered style was called"""
    pass
