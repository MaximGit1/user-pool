from logging import getLogger

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

log = getLogger(__name__)


class SQLAlchemyDBConnectionChecker:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def check(self) -> bool:
        try:
            result = await self._session.execute(text("SELECT 1"))
            return result.scalar() == 1
        except SQLAlchemyError as exc:
            err_msg = f"DB(QLAlchemy) connection check failed: {exc}"

            log.error(err_msg, extra={"trace": exc})

            return False
        except Exception as e:
            err_msg = f"Unexpected error during Redis check: {e}"
            log.critical(err_msg, extra={"trace": e})
            return False
