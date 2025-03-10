class APIException(Exception):
    """Base class for REST framework exceptions.
      Subclasses should provide `.status_code` and `.default_detail` properties.

    Args:

    Returns:

    """
    default_detail = ''
    default_code = 'error'

    def __init__(self, detail, code):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code

    def __str__(self):
        return str(self.detail)


class ServiceNotFoundException(APIException):
    """ """
    pass


class PermissionDeniedException(APIException):
    """ """
    pass


class InvalidClientRequestException(APIException):
    """ """
    pass


class ServerException(APIException):
    """ """
    pass
