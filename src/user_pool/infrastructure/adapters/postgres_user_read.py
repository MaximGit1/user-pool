from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination, SortOrder
from user_pool.application.common.repositories.user_mapper import UserMapper
from user_pool.domain.entities.user import User
from user_pool.domain.value_objects.user_id import UserID
from user_pool.infrastructure.db.models.users import users_table


class PostgresUserReadRepository:
    def __init__(self, session: AsyncSession, mapper: UserMapper) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_id(self, user_id: UserID) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id.value)

        result = await self._session.execute(stmt)
        row = result.mappings().one_or_none()
        return None if row is None else self._mapper.load_user(row)

    async def list(
        self, filters: UserFilter, pagination: Pagination
    ) -> list[User]:
        stmt = select(users_table)

        if filters.username:
            stmt = stmt.where(
                users_table.c.username.ilike(f"%{filters.username}%")
            )

        if filters.email:
            stmt = stmt.where(users_table.c.email.ilike(f"%{filters.email}%"))

        order_column = users_table.c.created_at

        if pagination.order is SortOrder.ASC:
            stmt = stmt.order_by(asc(order_column))
        else:
            stmt = stmt.order_by(desc(order_column))

        stmt = stmt.offset(pagination.offset).limit(pagination.limit)

        result = await self._session.execute(stmt)
        return self._mapper.load_users(result.mappings().all())
