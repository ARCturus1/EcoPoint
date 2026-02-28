from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from schemas import (
    CreateBinModel,
    GetBinModel,
    UpdateBinModel,
)
from common import BaseRepository
from models import BinOrm


class BinsData(BaseRepository[BinOrm, GetBinModel, CreateBinModel, UpdateBinModel]):
    model = BinOrm
    schema_response = GetBinModel
    schema_create = CreateBinModel
    schema_update = UpdateBinModel
