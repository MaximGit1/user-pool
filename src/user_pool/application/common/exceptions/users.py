from user_pool.application.common.exceptions.base import ApplicationError


class UserNotFoundError(ApplicationError):
    pass


class UserAlreadyLockedError(ApplicationError):
    pass


class UsernameAlreadyExistsError(ApplicationError):
    pass
