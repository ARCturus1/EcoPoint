# Add parent directory to Python path
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.errors import DuplicateException, MissingException
from fastapi import APIRouter, Body, HTTPException
from schemas import (
    CreateDepositModel,
    GetDepositModel,
    RequestCreateDepositModel,
    UpdateDepositModel,
    RequestUpdateDepositModel,
)
from service import DepositService


router = APIRouter(prefix="/api/deposit", tags=["Deposit"])
crudService = DepositService()


@router.get("")
async def get_deposits() -> list[GetDepositModel]:
    return await crudService.get_all() or []


@router.get("/{deposit_id}")
async def get_deposit(deposit_id: int) -> GetDepositModel | None:
    try:
        return await crudService.get_one(id=deposit_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("{user_id}")
async def create_deposit(
    user_id: int,
    deposit: RequestCreateDepositModel = Body(),
) -> GetDepositModel | None:
    try:
        depositDTO = CreateDepositModel(user_id=user_id, **vars(deposit))
        return await crudService.create(depositDTO)
    except DuplicateException as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.patch("/{user_id}/{deposit_id}")
async def update_deposit(
    user_id: int, deposit_id: int, deposit: RequestUpdateDepositModel
) -> GetDepositModel | None:
    try:
        depositDTO = UpdateDepositModel(user_id=user_id, **vars(deposit))
        return await crudService.modify(depositDTO, id=deposit_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{deposit_id}")
async def delete(deposit_id: int) -> bool:
    try:
        return await crudService.delete(id=deposit_id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
