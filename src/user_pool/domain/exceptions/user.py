from user_pool.domain.exceptions.base import DomainError


class UsernameRangeError(DomainError):
    """Used in Username VO validation"""


class UsernameValueError(DomainError):
    """Used in Username VO validation"""


class PasswordRangeError(DomainError):
    """Used in Password VO validation.
    Simulates a raw password that is converted into bytes
    """


class PasswordValueError(DomainError):
    """Used in Password VO validation.
    Simulates a raw password that is converted into bytes
    """


class EmailValueError(DomainError):
    """Used in Email VO validation"""


class UserAlreadyAssignedToProjectError(DomainError):
    """User is already assigned to a project."""
