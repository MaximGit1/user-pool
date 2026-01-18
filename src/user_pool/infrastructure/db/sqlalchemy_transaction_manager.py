from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyTransactionManager:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def flush(self) -> None:
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
