from logging import getLogger  # pragma: no cover

from user_pool.application.common.exceptions.services import (
    ServiceError,  # pragma: no cover
)
from user_pool.application.common.repositories.checkers import (
    CacheConnectionChecker,
    DBConnectionChecker,
)  # pragma: no cover

log = getLogger(__name__)  # pragma: no cover


class HealthRequestHandler:  # pragma: no cover
    def __init__(
        self,
        db: DBConnectionChecker,
        cache: CacheConnectionChecker,
    ) -> None:
        self._db = db
        self._cache = cache

    async def handle(self) -> None:
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
