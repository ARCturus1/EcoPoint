from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends

from common.errors import DuplicateException, MissingException
from schemas import (
    CreateBinModel,
    GetBinModel,
    UpdateBinModel,
)
from service import BinsService


router = APIRouter(prefix="/api/bins", tags=["Bins"])
crudService = BinsService()


@router.get("/health")
def health():
    return {"status": "OK"}


@router.get("")
async def get_bins() -> dict[str, list[GetBinModel] | int]:
    bins = await crudService.get_all() or []
    return {"bins": bins, "count": len(bins)}


@router.get("/{bin_id}")
async def get_bin(bin_id: int) -> GetBinModel | None:
    try:
        return await crudService.get_one(id=bin_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("")
async def create_bin(bin: CreateBinModel = Body()) -> GetBinModel | None:
    try:
        return await crudService.create(bin)
    except DuplicateException as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.patch("/{bin_id}")
async def update_bin(bin_id: int, bin: UpdateBinModel) -> GetBinModel | None:
    try:
        return await crudService.modify(bin, id=bin_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{bin_id}")
async def delete(bin_id: int) -> bool:
    try:
        return await crudService.delete(id=bin_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
