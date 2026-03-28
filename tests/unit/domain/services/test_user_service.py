from datetime import UTC, datetime
from uuid import uuid4

import pytest

from user_pool.domain.exceptions.user import (
    EmailValueError,
    PasswordValueError,
    UsernameRangeError,
)
from user_pool.domain.ports.password_hasher import PasswordHasher
from user_pool.domain.ports.user_id_generator import UserIDGenerator
from user_pool.domain.services import UserService
from user_pool.domain.value_objects import RawPassword, UserID


class MockUserIDGenerator(UserIDGenerator):
    def __init__(self) -> None:
        self.v = uuid4()

    def generate(self) -> UserID:
        return UserID.unsafe(self.v)

class MockPasswordHasher(PasswordHasher):
    def hash(self, raw_password: RawPassword) -> bytes:
        return raw_password.value.encode()


def test_user_service() -> None:
    service = UserService(
        id_generator=MockUserIDGenerator(),
        password_hasher=MockPasswordHasher(),
    )

    password = "my_Palswwrd19O_"
    time_stamp = datetime.now(UTC)

    user = service.create_user(
        username="my_username",
        email="valid_email6@gmail.com",
        raw_password=password,
    )

    assert user.id
    assert user.hashed_password == password.encode()
    assert user.created_at > time_stamp
    assert user.created_at < datetime.now(UTC)

    with pytest.raises(UsernameRangeError):
        service.create_user(
            "my",
            email="valid_email6@g",
            raw_password="jhgdfskalk",
        )

    with pytest.raises(EmailValueError):
        service.create_user(
            "my_username",
            email="valid_email6@g",
            raw_password="",
        )

    with pytest.raises(PasswordValueError):
        service.create_user(
            "my_username",
            email="valid_email6@gmail.com",
            raw_password="!^&#)(19",
        )
