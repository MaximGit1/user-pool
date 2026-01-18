from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user_pool.application.common.repositories import DBExceptionMapper
from user_pool.application.common.repositories.user_mapper import UserMapper
from user_pool.domain.entities import User
from user_pool.infrastructure.db.models.users import users_table


class PostgresUserWriteRepository:
    def __init__(
        self,
        session: AsyncSession,
        user_mapper: UserMapper,
        exception_mapper: DBExceptionMapper,
    ) -> None:
        self._session = session
        self._user_mapper = user_mapper
        self._exception_mapper = exception_mapper

    async def add(self, user: User) -> None:
        stmt = users_table.insert().values(
            **self._user_mapper.to_create_data(user)
        )

        try:
            await self._session.execute(stmt)
        except IntegrityError as exp:
            self._exception_mapper.map(exp)
