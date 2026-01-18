from user_pool.application.common.exceptions.users import (
    UsernameAlreadyExistsError,
)
from user_pool.application.common.repositories import ExceptionRule
from user_pool.infrastructure.db.constraint_rules import (
    IntegrityConstraintRule,
)


def init_exception_rules() -> list[ExceptionRule]:
    return [
        IntegrityConstraintRule(
            "uq_users_username",
            UsernameAlreadyExistsError,
            "User already exists",
        ),
    ]
