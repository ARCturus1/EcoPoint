import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database import database_path
from common.base import BaseRepository
from models import UserStatsOrm
from schemas import (
    CreateUserStatsModel,
    GetUserStatsModel,
    UpdateUserStatsModel,
)
from common.base import BaseService
from data import UserStatsData


class UserStatsService(
    BaseService[
        GetUserStatsModel, CreateUserStatsModel, UpdateUserStatsModel, UserStatsOrm
    ]
):
    dataCrud: BaseRepository[
        UserStatsOrm, GetUserStatsModel, CreateUserStatsModel, UpdateUserStatsModel
    ]

    def __init__(self) -> None:
        self.dataCrud = UserStatsData(database_path or "")
        super().__init__()

    schema_response = GetUserStatsModel
    schema_create = CreateUserStatsModel
    schema_update = UpdateUserStatsModel
