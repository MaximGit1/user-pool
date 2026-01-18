import sqlalchemy as sa

from user_pool.infrastructure.db.models.base import mapper_registry

users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("username", sa.String(20), nullable=False, unique=True),
    sa.Column("email", sa.String(60), nullable=False),
    sa.Column("password", sa.LargeBinary, nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=True,
    ),
)
