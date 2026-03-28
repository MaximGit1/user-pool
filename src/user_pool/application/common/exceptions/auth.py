from user_pool.application.common.exceptions.base import ApplicationError


class ClientAlreadyExistsError(ApplicationError):
    pass

class ClientNotFoundError(ApplicationError):
    pass

class InvalidArgument(ApplicationError):
    pass

class UnauthenticatedError(ApplicationError):
    pass

class InvalidTokenError(ApplicationError):
    pass

class InternalError(ApplicationError):
    pass

