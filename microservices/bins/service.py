from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common import BaseRepository
from common import BaseService
from data import BinsData
from models import BinOrm
from schemas import CreateBinModel, GetBinModel, UpdateBinModel
from database import database_path


class BinsService(
    BaseService[
        GetBinModel,
        CreateBinModel,
        UpdateBinModel,
        BinOrm,
    ]
):
    dataCrud: BaseRepository[BinOrm, GetBinModel, CreateBinModel, UpdateBinModel]

    def __init__(self) -> None:
        self.dataCrud = BinsData(database_path or "")
        super().__init__()
        self.schema_response = GetBinModel
        self.schema_create = CreateBinModel
        self.schema_update = UpdateBinModel
