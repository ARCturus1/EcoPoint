from pydantic import BaseModel

# from app.feature.auth.models.user import UserModel


class GetUserStatsModel(BaseModel):
    id: int
    totalDeposits: float | None
    plasticKg: float | None
    paperKg: float | None
    userId: int | None
    # users: list[UserModel] | None


class CreateUserStatsModel(BaseModel):
    totalDeposits: float | None
    plasticKg: float | None
    paperKg: float | None
    userId: int | None


class UpdateUserStatsModel(BaseModel):
    totalDeposits: float | None = None
    plasticKg: float | None = None
    paperKg: float | None = None
