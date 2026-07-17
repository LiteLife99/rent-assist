from typing import Literal

from pydantic.dataclasses import dataclass

from rent_assist.infra.exceptions.models import RentAssistError


@dataclass(slots=True)
class DemoItemNotFoundError(RentAssistError):
    message: str = "Demo item not found"
    error_code: str = "DEMO_ITEM_NOT_FOUND"
    status_code: Literal[404] = 404
