class MagicJsonError(Exception):
    """Base error for all MagicJson Errors"""


class RegistrationError(MagicJsonError):
    """Error with registering a class method"""
