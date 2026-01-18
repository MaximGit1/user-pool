from typing import Protocol


class CacheConnectionChecker(Protocol):
    async def check(self) -> bool: ...
