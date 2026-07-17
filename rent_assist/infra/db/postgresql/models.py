"""Models for the database"""

import datetime
import decimal
import logging
import uuid
from typing import Any

from sqlalchemy import MetaData, text, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

try:
    from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
except ImportError:
    logging.info("PostgreSQL types not available. Using SQLAlchemy core types.")
    UUID = types.UUID
    JSONB = types.JSON
    ARRAY = types.ARRAY

convention = {
    "all_column_names": lambda constraint, _: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=convention)

    type_annotation_map = {
        bool: types.Boolean(),
        bytes: types.LargeBinary(),
        datetime.date: types.Date(),
        datetime.datetime: types.DateTime(timezone=True),
        datetime.time: types.Time(timezone=True),
        datetime.timedelta: types.Interval(),
        decimal.Decimal: types.Numeric(),
        float: types.Float(),
        int: types.Integer(),
        str: types.String(),
        uuid.UUID: UUID,
        dict: JSONB,
        dict[str, Any]: JSONB,
        list[str]: ARRAY(types.String()),
    }


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))


class AutoIncrementPrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=func.now())

    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )


class DeletedMixin:
    deleted: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="False")


class BaseSQLModel(TimestampMixin, UUIDPrimaryKeyMixin, DeletedMixin, Base):
    """
    Base model which defines shared fields and methods
    """

    __abstract__ = True


class BaseSQLModelWithAutoIncrementPrimaryKey(TimestampMixin, AutoIncrementPrimaryKeyMixin, DeletedMixin, Base):
    """
    Base model which defines shared fields and methods with an auto-incrementing primary key
    """

    __abstract__ = True
