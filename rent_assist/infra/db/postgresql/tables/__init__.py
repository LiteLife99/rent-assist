from rent_assist.infra.db.postgresql import models
from rent_assist.infra.db.postgresql.tables.demo_items_table import DemoItemsTable

Base = models.Base
BaseSQLModel = models.BaseSQLModel
DeletedMixin = models.DeletedMixin
TimestampMixin = models.TimestampMixin
UUIDPrimaryKeyMixin = models.UUIDPrimaryKeyMixin

__all__ = [
    "Base",
    "BaseSQLModel",
    "DeletedMixin",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "DemoItemsTable",
]
