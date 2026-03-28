import pytest

from user_pool.domain.exceptions.user import (
    UsernameRangeError,
    UsernameValueError,
)
from user_pool.domain.value_objects.username import Username


@pytest.mark.parametrize("value", ["ValidName", "valid_name", "_VaLiD_nAmE_"])
def test_valid_create(value: str) -> None:
    vo = Username.safe(value)

    assert vo.value == value


@pytest.mark.parametrize("value", ["v" * 4, "v" * 21])
def test_range_err_create(value: str) -> None:
    with pytest.raises(UsernameRangeError) as exp:
        Username.safe(value)

        assert isinstance(exp.value, UsernameRangeError)


@pytest.mark.parametrize("value", ["1ValidName", "valid_name!"])
def test_value_err_create(value: str) -> None:
    with pytest.raises(UsernameValueError) as exp:
        Username.safe(value)

        assert isinstance(exp.value, UsernameValueError)
