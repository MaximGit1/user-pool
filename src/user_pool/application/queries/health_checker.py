from logging import getLogger
from typing import Protocol

from bazario import Request
from bazario.asyncio import RequestHandler

from user_pool.application.common.exceptions.services import ServiceError
from user_pool.application.common.repositories.checkers import (
        CacheConnectionChecker,
        DBConnectionChecker,
    )


log = getLogger(__name__)


class Service(Protocol):
    async def check(self) -> bool: ...


class RetrieveHealthRequest(Request[None]):
    pass


class RetrieveHealthRequestHandler(
    RequestHandler[RetrieveHealthRequest, None]
):
    def __init__(
        self,
        db: DBConnectionChecker,
        cache: CacheConnectionChecker,
    ) -> None:
        self._db = db
        self._cache = cache

    async def handle(self, request: RetrieveHealthRequest) -> None:
        try:
            if not (await self._db.check() and await self._cache.check()):
                msg = "application is temporarily unavailable."

                log.warning(msg)

                raise ServiceError(msg) from None
        except Exception as e:
            err = str(e)

            log.critical(err)

            msg = "service is temporarily unresponsive"

            raise ServiceError(msg) from e
