from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Body, HTTPException, Header
from common.errors import MissingException
from schemas import CreateUserStatsModel, GetUserStatsModel, UpdateUserStatsModel
from services import UserStatsService


router = APIRouter(prefix="/api/user-stats", tags=["User Stats"])

crudUserStats = UserStatsService()


@router.get("/health")
def health():
    return {"status": "OK"}


@router.get("")
async def get_all() -> dict[str, list[GetUserStatsModel] | int]:
    stats = await crudUserStats.get_all()
    return {"stats": stats, "count": len(stats)}


@router.get("/get_by_user_id")
async def get_by_user_id(x_user_id: str = Header()) -> GetUserStatsModel | None:
    try:
        result = await crudUserStats.get_one(userId=x_user_id)
        return result
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.get("/{id}")
async def get_one(id: int) -> GetUserStatsModel | None:
    try:
        result = await crudUserStats.get_one(userId=id)
        return result
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("")
async def create(
    userStats: CreateUserStatsModel = Body(None),
) -> GetUserStatsModel | None:
    return await crudUserStats.create(userStats)


@router.patch("/{id}")
async def update_user_stats(
    id: int, user_stats: UpdateUserStatsModel
) -> GetUserStatsModel | None:
    try:
        return await crudUserStats.modify(user_stats, id=id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{id}")
async def delete_user_stats(id: int) -> bool:
    try:
        return await crudUserStats.delete(id=id)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)
