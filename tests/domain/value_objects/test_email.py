import pytest

from user_pool.domain.value_objects.email import Email
from user_pool.domain.exceptions.user import EmailValueError



@pytest.mark.parametrize(
    "value",
    [
        "user@example.com",
        "user.name@example.com",
        "user_name@example.com",
        "user+tag@example.com",
        "user-1@example-domain.com",
        "u123@example.co.uk",
    ],
)
def test_email_valid_create(value: str) -> None:
    email = Email.safe(value)

    assert email.value == value


@pytest.mark.parametrize(
    "value",
    [
        "plainaddress",
        "@example.com",
        "user@",
        "user@example",
        "user@example.",
        "user@.com",
        "user@@example.com",
        "user@exa mple.com",
    ],
)
def test_invalid_create(value: str) -> None:
    with pytest.raises(EmailValueError) as exp:
        Email.safe(value)

    assert isinstance(exp.value, EmailValueError)