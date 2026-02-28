from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from common import SqlAlchemyBase


class UserStatsOrm(SqlAlchemyBase):
    __tablename__ = "user_stats"

    totalDeposits: Mapped[float] = mapped_column(default=0.0)
    plasticKg: Mapped[float] = mapped_column(default=0.0)
    paperKg: Mapped[float] = mapped_column(default=0.0)
    userId: Mapped[int] = mapped_column(unique=True)
    # users: Mapped[UserOrm] = relationship(back_populates="userStats", lazy="joined")
