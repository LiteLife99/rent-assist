from pydantic import BaseModel

from rent_assist.modules.demo.data_models import BaseDemoItem, DemoItem


class CreateDemoItemRequest(BaseDemoItem):
    pass


class UpdateDemoItemRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    meta: dict | None = None


class DemoItemResponse(BaseModel):
    success: bool
    error: str | None = None
    item: DemoItem | None = None


class DemoItemListResponse(BaseModel):
    success: bool
    error: str | None = None
    items: list[DemoItem] = []
    total: int = 0
