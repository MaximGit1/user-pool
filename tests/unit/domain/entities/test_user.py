from datetime import UTC, datetime
from uuid import uuid4

from user_pool.domain.entities import User
from user_pool.domain.value_objects import Email, UserID, Username


def test_get_properties() -> None:
    username = "custom_username"
    created_at = datetime.now(UTC)
    hashed_password = b"AJKHD_8912eqfs"
    email = "myemail@gmail.com"

    user = User(
        _id=UserID.unsafe(uuid4()),
        _username=Username.unsafe(username),
        _created_at=created_at,
        _hashed_password=hashed_password,
        _email=Email.unsafe(email),
    )

    assert user.username.value == username
    assert user.created_at == created_at
    assert user.hashed_password == hashed_password
    assert user.email.value == email
