from abc import ABC
from dataclasses import dataclass
from typing import Generic, Self, TypeVar

ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class ValueObject(ABC, Generic[ValueT]):
    """Base VO class"""

    value: ValueT

    @classmethod
    def safe(cls, value: ValueT) -> Self:
        """Creates a new VO with validation"""
        cls._validate(value)
        return cls(value)

    @classmethod
    def unsafe(cls, value: ValueT) -> Self:
        """Used only for loading data from DB — no validation."""
        return cls(value)

    @classmethod
    def _validate(cls, value: ValueT) -> None:
        """Must be implemented by subclasses.
        Raises a :class:`DomainError` if the value is invalid.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __str__(self) -> str:
        return str(self.value)
