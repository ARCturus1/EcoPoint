# Add parent directory to Python path
from pathlib import Path
import sys
from typing import Any


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from schemas import (
    GetDepositModel,
    CreateDepositModel,
    UpdateDepositModel,
)
from models import DepositOrm
from common import BaseRepository


class DepositData(
    BaseRepository[DepositOrm, GetDepositModel, CreateDepositModel, UpdateDepositModel]
):
    def __init__(self, database_name: str, **kwargs: Any) -> None:
        super().__init__(database_name, **kwargs)
        self.model = DepositOrm
        self.schema_response = GetDepositModel
        self.schema_create = CreateDepositModel
        self.schema_update = UpdateDepositModel
