class MagicJSONError(Exception):
    """Base error for all MagicJson Errors"""


class RegistrationError(MagicJSONError):
    """Error with registering a class method"""


class MissingDeserializerError(MagicJSONError):
    """Attempt to deserialize with an unregistered method"""
