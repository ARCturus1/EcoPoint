# Add parent directory to Python path
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data import DepositData
from models import DepositOrm
from schemas import CreateDepositModel, GetDepositModel, UpdateDepositModel
from common import BaseService, BaseRepository
from database import database_path


class DepositService(
    BaseService[
        GetDepositModel,
        CreateDepositModel,
        UpdateDepositModel,
        DepositOrm,
    ]
):
    dataCrud: BaseRepository[
        DepositOrm, GetDepositModel, CreateDepositModel, UpdateDepositModel
    ]

    def __init__(self) -> None:
        self.dataCrud = DepositData(database_path)
        super().__init__()
        self.schema_response = GetDepositModel
        self.schema_create = CreateDepositModel
        self.schema_update = UpdateDepositModel
