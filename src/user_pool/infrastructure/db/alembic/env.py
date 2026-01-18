import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from user_pool.infrastructure.db.models.base import metadata
from user_pool.setup.config import DBConfig, create_config

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = metadata


def load_db_config() -> DBConfig:
    return create_config().db


def run_migrations_offline(db_config: DBConfig) -> None:
    """Run migrations in 'offline' mode."""

    url = db_config.uri

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online(db_config: DBConfig) -> None:
    """Run migrations in 'online' async mode."""
    url = db_config.uri

    connectable: AsyncEngine = create_async_engine(
        url, poolclass=pool.NullPool, future=True
    )

    async with connectable.connect() as connection:
        async with connection.begin():
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
            )
            await connection.run_sync(
                lambda sync_conn: context.run_migrations()
            )

        await connectable.dispose()

    await connectable.dispose()


def run_migrations() -> None:
    db_config = load_db_config()

    if context.is_offline_mode():
        run_migrations_offline(db_config)
    else:
        asyncio.run(run_migrations_online(db_config))


run_migrations()
