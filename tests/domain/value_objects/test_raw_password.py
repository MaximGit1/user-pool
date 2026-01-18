import pytest

from user_pool.domain.value_objects.raw_password import RawPassword
from user_pool.domain.exceptions.user import (
    PasswordRangeError,
    PasswordValueError,
)


@pytest.mark.parametrize("value", ["lorem09_$", "qwerty_passWord123!%"])
def test_valid_create(value: str) -> None:
    RawPassword.safe(value)


@pytest.mark.parametrize("value", ["1"*7, "l"*37])
def test_range_err_create(value: str) -> None:
    with pytest.raises(PasswordRangeError) as exp:
        RawPassword.safe(value)

    assert  isinstance(exp.value, PasswordRangeError)


@pytest.mark.parametrize("value", ["lorem09_$@11", "23тест032-"])
def test_value_err_create(value: str) -> None:
    with pytest.raises(PasswordValueError) as exp:
        RawPassword.safe(value)

    assert  isinstance(exp.value, PasswordValueError)

