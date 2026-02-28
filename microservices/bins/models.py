from pathlib import Path
import sys

from sqlalchemy import String, DECIMAL, DateTime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from common import SqlAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import datetime as dt


class BinOrm(SqlAlchemyBase):
    __tablename__ = "bins"

    name: Mapped[str] = mapped_column(String(length=100))
    qr_code: Mapped[str] = mapped_column(String(length=100), unique=True)
    address: Mapped[str]
    lat: Mapped[DECIMAL] = mapped_column(DECIMAL(9, 6))
    lng: Mapped[DECIMAL] = mapped_column(DECIMAL(9, 6))
    accepted_waste_types: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    installed_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # deposits: Mapped["DepositOrm"] = relationship(back_populates="bins")  # type: ignore
