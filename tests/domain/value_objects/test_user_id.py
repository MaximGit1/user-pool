from uuid import uuid4

from user_pool.domain.value_objects.user_id import UserID


def test_to_uuid() -> None:
    raw_id = uuid4()

    vo = UserID.safe(raw_id)

    assert vo.to_uuid() == raw_id
