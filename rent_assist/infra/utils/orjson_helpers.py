import logging
from typing import Literal, overload

from orjson import OPT_NON_STR_KEYS, OPT_SERIALIZE_NUMPY, dumps
from pydantic import BaseModel

try:
    from asyncpg.pgproto.pgproto import UUID as PGPROTO_UUID

    UUID_TYPE = PGPROTO_UUID
    HAS_ASYNCPG = True
except ImportError:
    logging.info("asyncpg not installed, PGPROTO_UUID type will not be handled")
    UUID_TYPE = type(None)
    HAS_ASYNCPG = False


class OrjsonHelpers:
    @staticmethod
    def orjson_dump_bytes(v, *, default) -> bytes:
        return dumps(v, default=default, option=OPT_NON_STR_KEYS | OPT_SERIALIZE_NUMPY)

    @staticmethod
    def orjson_dumps(v, *, default) -> str:
        return OrjsonHelpers.orjson_dump_bytes(v, default=default).decode()

    @staticmethod
    @overload
    def serialize(data: dict, return_bytes: Literal[True]) -> bytes: ...

    @staticmethod
    @overload
    def serialize(data: dict, return_bytes: Literal[False]) -> str: ...

    @staticmethod
    def serialize(data, return_bytes: bool) -> bytes | str:
        if return_bytes:
            return OrjsonHelpers.orjson_dump_bytes(data, default=OrjsonHelpers.default)
        return OrjsonHelpers.orjson_dumps(data, default=OrjsonHelpers.default)

    @staticmethod
    def default(obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if HAS_ASYNCPG and isinstance(obj, UUID_TYPE):
            return str(obj)
        return obj
