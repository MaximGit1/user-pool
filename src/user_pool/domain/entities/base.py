from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from user_pool.domain.value_objects.base import ValueObject

EntityId = TypeVar("EntityId", bound=ValueObject[Any])


@dataclass(slots=True)
class BaseEntity(ABC, Generic[EntityId]):
    """Base class for domain entities, defined by a unique identity `id`"""

    _id: EntityId

    @property
    def id(self) -> EntityId:
        """Returns entity id"""
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented

        if type(self) is not type(other):
            return False

        return self.id == other.id

    def __hash__(self) -> int:  # pragma: no cover
        return hash((type(self), self._id))

    def __repr__(self) -> str:  # pragma: no cover
        return f"{type(self).__name__}(id_={self._id!r})"
