class MagicJsonError(Exception):
    """Base error for all MagicJson Errors"""


class RegistrationError(MagicJsonError):
    """Error with registering a class method"""


class MissingDeserializerError(MagicJsonError):
    """Attempt to deserialize with an unregistered method"""
