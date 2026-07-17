from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from rent_assist.infra.db.postgresql.models import BaseSQLModel


class DemoItemsTable(BaseSQLModel):
    __tablename__ = "demo_items"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    meta: Mapped[dict | None] = mapped_column(JSONB(), nullable=True)
