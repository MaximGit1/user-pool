from typing import Protocol


class DBConnectionChecker(Protocol):
    async def check(self) -> bool: ...
