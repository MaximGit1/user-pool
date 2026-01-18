from dataclasses import dataclass
import pytest

from user_pool.domain.value_objects.base import ValueObject, ValueT


ERR_VALUE = "error throw"


@dataclass(frozen=True)
class MockVO(ValueObject[str]):
    @classmethod
    def _validate(cls, value: ValueT) -> None:
        if value == ERR_VALUE:
            raise ValueError


@pytest.mark.parametrize("value", ["test value", ERR_VALUE])
def test_unsafe_create(value: str) -> None:
    vo = MockVO.unsafe(value)

    assert vo.value == value


def test_safe_create() -> None:
    with pytest.raises(ValueError) as exp:
        MockVO.safe(ERR_VALUE)

    assert isinstance(exp.value, ValueError)
