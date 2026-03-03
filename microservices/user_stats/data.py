from typing import Any

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
    def __init__(self, database_name: str, **kwargs: Any) -> None:
        super().__init__(database_name, **kwargs)
        self.model = UserStatsOrm
        self.schema_response = GetUserStatsModel
        self.schema_create = CreateUserStatsModel
        self.schema_update = UpdateUserStatsModel
