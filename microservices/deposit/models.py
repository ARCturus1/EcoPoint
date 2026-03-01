from common import SqlAlchemyBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
import datetime as dt


class DepositOrm(SqlAlchemyBase):
    __tablename__ = "deposits"

    user_id: Mapped[int]  # Кто сдал
    # users: Mapped["UserOrm"] = relationship(back_populates="deposits")  # type: ignore
    bin_id: Mapped[int]  # Кто сдал
    # bins: Mapped["BinOrm"] = relationship(back_populates="deposits")  # type: ignore
    waste_type: Mapped[str] = mapped_column(String(20))
    weight_kg: Mapped[float] = mapped_column(default=0.0)
    eco_points_earned: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
