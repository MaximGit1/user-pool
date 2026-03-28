from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from user_pool.application.common.repositories import (
    AssignedUserReadRepository,
    AssignedUserWriteRepository,
    DBExceptionMapper,
    ExceptionRule,
    UserReadRepository,
    UserWriteRepository,
)
from user_pool.application.common.repositories.checkers import (
    DBConnectionChecker,
)
from user_pool.application.common.repositories.transaction_manager import (
    TransactionManager,
)
from user_pool.application.common.repositories.user_mapper import UserMapper
from user_pool.infrastructure.adapters import (
    PostgresUserReadRepository,
    PostgresUserWriteRepository,
    RedisAssignedUserReadRepository,
    RedisAssignedUserWriteRepository,
)
from user_pool.infrastructure.adapters.sqlalchemy_connection_checker import (
    SQLAlchemyDBConnectionChecker,
)
from user_pool.infrastructure.adapters.sqlalchemy_user_mapper import (
    SqlalchemyUserMapper,
)
from user_pool.infrastructure.db.exception_rules import init_exception_rules
from user_pool.infrastructure.db.sqlalchemy_exception_mapper import (
    SqlAlchemyExceptionMapper,
)
from user_pool.infrastructure.db.sqlalchemy_transaction_manager import (
    SqlAlchemyTransactionManager,
)
from user_pool.setup.config import DBConfig


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_engine(
        self, config: DBConfig
    ) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            config.uri,
            echo=config.debug,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
        )

        yield engine

        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_transaction(
        self,
        session: AsyncSession,
    ) -> AsyncIterator[TransactionManager]:
        async with session.begin():
            yield SqlAlchemyTransactionManager(session)


def db_utils_provider() -> Provider:
    provider = Provider()

    provider.provide(
        SqlAlchemyExceptionMapper,
        scope=Scope.APP,
        provides=DBExceptionMapper,
    )

    provider.provide(
        SqlAlchemyTransactionManager,
        scope=Scope.REQUEST,
        provides=TransactionManager,
    )

    provider.provide(
        init_exception_rules,
        scope=Scope.APP,
        provides=list[ExceptionRule],
    )

    return provider


def repository_read_provider() -> Provider:
    provider = Provider()

    provider.provide(
        RedisAssignedUserReadRepository,
        scope=Scope.REQUEST,
        provides=AssignedUserReadRepository,
    )

    provider.provide(
        PostgresUserReadRepository,
        scope=Scope.REQUEST,
        provides=UserReadRepository,
    )

    return provider


def repository_write_provider() -> Provider:
    provider = Provider()

    provider.provide(
        RedisAssignedUserWriteRepository,
        scope=Scope.REQUEST,
        provides=AssignedUserWriteRepository,
    )

    provider.provide(
        PostgresUserWriteRepository,
        scope=Scope.REQUEST,
        provides=UserWriteRepository,
    )

    return provider


def mapper_provider() -> Provider:
    provider = Provider(scope=Scope.APP)

    provider.provide(SqlalchemyUserMapper, provides=UserMapper)

    return provider


def db_checker_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(
        SQLAlchemyDBConnectionChecker, provides=DBConnectionChecker
    )

    return provider


def get_db_providers() -> list[Provider]:
    return [
        DBProvider(),
        db_utils_provider(),
        repository_read_provider(),
        repository_write_provider(),
        mapper_provider(),
        db_checker_provider(),
    ]
