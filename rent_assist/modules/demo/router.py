from typing import Annotated
from uuid import UUID

from fastapi import APIRouter

from rent_assist.application.depends import Depends
from rent_assist.application.di.main import di_get_demo_service
from rent_assist.modules.demo.dto import (
    CreateDemoItemRequest,
    DemoItemListResponse,
    DemoItemResponse,
    UpdateDemoItemRequest,
)
from rent_assist.modules.demo.exceptions import DemoItemNotFoundError
from rent_assist.modules.demo.service import DemoService

router = APIRouter(tags=["demo"])


@router.get(
    "/items",
    response_model=DemoItemListResponse,
)
async def list_items(
    demo_service: Annotated[DemoService, Depends(di_get_demo_service)],
) -> DemoItemListResponse:
    try:
        items = await demo_service.list_items()
        return DemoItemListResponse(success=True, items=items, total=len(items))
    except Exception as e:
        return DemoItemListResponse(success=False, error=f"Unexpected error: {str(e)}")


@router.get(
    "/items/{item_id}",
    response_model=DemoItemResponse,
)
async def get_item(
    item_id: UUID,
    demo_service: Annotated[DemoService, Depends(di_get_demo_service)],
) -> DemoItemResponse:
    try:
        item = await demo_service.get_item(item_id)
        return DemoItemResponse(success=True, item=item)
    except DemoItemNotFoundError as e:
        return DemoItemResponse(success=False, error=str(e))
    except Exception as e:
        return DemoItemResponse(success=False, error=f"Unexpected error: {str(e)}")


@router.post(
    "/items",
    response_model=DemoItemResponse,
    status_code=201,
)
async def create_item(
    request: CreateDemoItemRequest,
    demo_service: Annotated[DemoService, Depends(di_get_demo_service)],
) -> DemoItemResponse:
    try:
        item = await demo_service.create_item(request)
        return DemoItemResponse(success=True, item=item)
    except Exception as e:
        return DemoItemResponse(success=False, error=f"Unexpected error: {str(e)}")


@router.put(
    "/items/{item_id}",
    response_model=DemoItemResponse,
)
async def update_item(
    item_id: UUID,
    request: UpdateDemoItemRequest,
    demo_service: Annotated[DemoService, Depends(di_get_demo_service)],
) -> DemoItemResponse:
    try:
        item = await demo_service.update_item(item_id, request)
        return DemoItemResponse(success=True, item=item)
    except DemoItemNotFoundError as e:
        return DemoItemResponse(success=False, error=str(e))
    except Exception as e:
        return DemoItemResponse(success=False, error=f"Unexpected error: {str(e)}")


@router.delete(
    "/items/{item_id}",
    response_model=DemoItemResponse,
)
async def delete_item(
    item_id: UUID,
    demo_service: Annotated[DemoService, Depends(di_get_demo_service)],
) -> DemoItemResponse:
    try:
        item = await demo_service.delete_item(item_id)
        return DemoItemResponse(success=True, item=item)
    except DemoItemNotFoundError as e:
        return DemoItemResponse(success=False, error=str(e))
    except Exception as e:
        return DemoItemResponse(success=False, error=f"Unexpected error: {str(e)}")
