from sqlalchemy import MetaData
from sqlalchemy.orm import registry

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)
"""Central SQLAlchemy metadata instance with standardized naming conventions.

Naming conventions:
    - ix: Index names (ix_<column_label>)
    - uq: Unique constraint names (uq_<table>_<column>)
    - ck: Check constraint names (ck_<table>_<constraint>)
    - fk: Foreign key names (fk_<table>_<column>_<reftable>)
    - pk: Primary key names (pk_<table>)
"""

mapper_registry = registry(metadata=metadata)
