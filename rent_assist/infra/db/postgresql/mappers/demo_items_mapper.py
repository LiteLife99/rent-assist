from rent_assist.infra.db.postgresql.tables.demo_items_table import DemoItemsTable
from rent_assist.modules.demo.data_models import BaseDemoItem, DemoItem


class DemoItemsMapper:
    @classmethod
    def to_domain(cls, record: DemoItemsTable) -> DemoItem:
        return DemoItem(
            id=record.id,
            name=record.name,
            description=record.description,
            is_active=record.is_active,
            meta=record.meta,
            created_at=record.created_at,
            updated_at=record.updated_at,
            deleted=record.deleted,
        )

    @classmethod
    def to_record(cls, domain_obj: DemoItem, record: DemoItemsTable | None = None) -> DemoItemsTable:
        if record is None:
            record = DemoItemsTable(
                id=domain_obj.id,
                name=domain_obj.name,
                description=domain_obj.description,
                is_active=domain_obj.is_active,
                meta=domain_obj.meta,
                created_at=domain_obj.created_at,
                updated_at=domain_obj.updated_at,
                deleted=domain_obj.deleted,
            )
        else:
            record.name = domain_obj.name
            record.description = domain_obj.description
            record.is_active = domain_obj.is_active
            record.meta = domain_obj.meta
            record.updated_at = domain_obj.updated_at
            record.deleted = domain_obj.deleted

        return record

    @classmethod
    def to_record_from_base(cls, base: BaseDemoItem) -> DemoItemsTable:
        return DemoItemsTable(
            name=base.name,
            description=base.description,
            is_active=base.is_active,
            meta=base.meta,
        )
