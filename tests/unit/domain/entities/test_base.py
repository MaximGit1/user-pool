from user_pool.domain.entities.base import BaseEntity
from user_pool.domain.value_objects.base import ValueObject


class MockID(ValueObject[int]):
    pass

class MockEntity(BaseEntity[MockID]):
    pass


def test_create_entity() -> None:
    _ = MockEntity(MockID(1))


def test_id_getter() -> None:
    id_ = MockID(1)
    entity = MockEntity(id_)

    assert entity.id == id_
    assert isinstance(entity.id, MockID)


def test_eq() -> None:
    class AnyObj:
        pass

    class AnyMockEntity(BaseEntity[MockID]):
        pass

    entity = MockEntity(MockID(1))
    entity2 = MockEntity(MockID(1))
    entity3 = MockEntity(MockID(2))

    assert entity == entity
    assert entity == entity2
    assert entity != entity3
    assert entity != AnyObj()
    assert entity != AnyMockEntity(MockID(1))
