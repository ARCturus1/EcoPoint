# Add parent directory to Python path
from pathlib import Path
import sys


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
    model = DepositOrm
    schema_response = GetDepositModel
    schema_create = CreateDepositModel
    schema_update = UpdateDepositModel
