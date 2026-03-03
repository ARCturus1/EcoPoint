from pathlib import Path
import sys
from typing import Any


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from schemas import (
    CreateBinModel,
    GetBinModel,
    UpdateBinModel,
)
from common import BaseRepository
from models import BinOrm


class BinsData(BaseRepository[BinOrm, GetBinModel, CreateBinModel, UpdateBinModel]):
    def __init__(self, database_name: str, **kwargs: Any) -> None:
        super().__init__(database_name, **kwargs)
        self.model = BinOrm
        self.schema_response = GetBinModel
        self.schema_create = CreateBinModel
        self.schema_update = UpdateBinModel
