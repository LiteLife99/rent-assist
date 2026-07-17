import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class BaseDemoItem(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True
    meta: dict[str, Any] | None = None


class DemoItem(BaseDemoItem):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted: bool = False
