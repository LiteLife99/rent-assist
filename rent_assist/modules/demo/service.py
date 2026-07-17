from uuid import UUID

from rent_assist.infra.db.postgresql.repositories.demo_items_repository import DemoItemsRepository
from rent_assist.modules.demo.data_models import BaseDemoItem, DemoItem
from rent_assist.modules.demo.dto import CreateDemoItemRequest, UpdateDemoItemRequest
from rent_assist.modules.demo.exceptions import DemoItemNotFoundError


class DemoService:
    def __init__(self, demo_items_repository: DemoItemsRepository):
        self._repo = demo_items_repository

    async def create_item(self, request: CreateDemoItemRequest) -> DemoItem:
        base = BaseDemoItem(
            name=request.name,
            description=request.description,
            is_active=request.is_active,
            meta=request.meta,
        )
        return await self._repo.create(base)

    async def get_item(self, item_id: UUID) -> DemoItem:
        item = await self._repo.find_by_id(item_id)
        if not item:
            raise DemoItemNotFoundError(
                message=f"Demo item with id {item_id} not found",
                detail={"item_id": str(item_id)},
            )
        return item

    async def list_items(self) -> list[DemoItem]:
        return await self._repo.find_all()

    async def update_item(self, item_id: UUID, request: UpdateDemoItemRequest) -> DemoItem:
        existing = await self._repo.find_by_id(item_id)
        if not existing:
            raise DemoItemNotFoundError(
                message=f"Demo item with id {item_id} not found",
                detail={"item_id": str(item_id)},
            )

        updated = DemoItem(
            id=existing.id,
            name=request.name if request.name is not None else existing.name,
            description=request.description if request.description is not None else existing.description,
            is_active=request.is_active if request.is_active is not None else existing.is_active,
            meta=request.meta if request.meta is not None else existing.meta,
            created_at=existing.created_at,
            updated_at=existing.updated_at,
            deleted=existing.deleted,
        )

        return await self._repo.update(updated)

    async def delete_item(self, item_id: UUID) -> DemoItem:
        existing = await self._repo.find_by_id(item_id)
        if not existing:
            raise DemoItemNotFoundError(
                message=f"Demo item with id {item_id} not found",
                detail={"item_id": str(item_id)},
            )
        return await self._repo.soft_delete(item_id)
