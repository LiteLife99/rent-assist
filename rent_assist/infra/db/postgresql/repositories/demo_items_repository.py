from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from rent_assist.infra.db.postgresql.mappers.demo_items_mapper import DemoItemsMapper
from rent_assist.infra.db.postgresql.tables.demo_items_table import DemoItemsTable
from rent_assist.modules.demo.data_models import BaseDemoItem, DemoItem


class DemoItemsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, base: BaseDemoItem) -> DemoItem:
        db_item = DemoItemsMapper.to_record_from_base(base)
        self._session.add(db_item)
        await self._session.flush()
        await self._session.refresh(db_item)
        await self._session.commit()
        return DemoItemsMapper.to_domain(db_item)

    async def find_by_id(self, item_id: UUID) -> DemoItem | None:
        query = select(DemoItemsTable).where(
            DemoItemsTable.id == item_id,
            DemoItemsTable.deleted == False,  # noqa: E712
        )
        result = await self._session.execute(query)
        item = result.scalars().first()
        return DemoItemsMapper.to_domain(item) if item else None

    async def find_all(self) -> list[DemoItem]:
        query = select(DemoItemsTable).where(
            DemoItemsTable.deleted == False,  # noqa: E712
        )
        result = await self._session.execute(query)
        items = result.scalars().all()
        return [DemoItemsMapper.to_domain(item) for item in items]

    async def update(self, item: DemoItem) -> DemoItem:
        query = select(DemoItemsTable).where(DemoItemsTable.id == item.id)
        result = await self._session.execute(query)
        db_item = result.scalars().first()

        if db_item is None:
            raise ValueError(f"DemoItem with id {item.id} not found")

        DemoItemsMapper.to_record(item, db_item)
        await self._session.commit()
        await self._session.refresh(db_item)
        return DemoItemsMapper.to_domain(db_item)

    async def soft_delete(self, item_id: UUID) -> DemoItem:
        update_query = (
            update(DemoItemsTable).where(DemoItemsTable.id == item_id).values(deleted=True).returning(DemoItemsTable)
        )
        result = await self._session.execute(update_query)
        await self._session.commit()
        updated_record = result.scalars().first()

        if updated_record is None:
            raise ValueError(f"DemoItem with id {item_id} not found")

        return DemoItemsMapper.to_domain(updated_record)
