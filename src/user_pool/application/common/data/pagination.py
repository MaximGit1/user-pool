from enum import StrEnum


class SortOrder(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class Pagination:
    def __init__(
        self,
        offset: int | None = None,
        limit: int | None = None,
        order: SortOrder | None = None,
    ) -> None:
        self.offset = 0 if offset is None else offset
        self.limit = 20 if limit is None else limit
        self.order = SortOrder.ASC if order is None else order
