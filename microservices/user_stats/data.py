from common.base.data import BaseRepository
from models import UserStatsOrm
from schemas import (
    GetUserStatsModel,
    CreateUserStatsModel,
    UpdateUserStatsModel,
)


class UserStatsData(
    BaseRepository[
        UserStatsOrm, GetUserStatsModel, CreateUserStatsModel, UpdateUserStatsModel
    ]
):
    model = UserStatsOrm
    schema_response = GetUserStatsModel
    schema_create = CreateUserStatsModel
    schema_update = UpdateUserStatsModel
