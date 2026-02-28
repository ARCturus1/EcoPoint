from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from common import SqlAlchemyBase


class UserOrm(SqlAlchemyBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    hash: Mapped[str]
    name: Mapped[str]
    phone: Mapped[str | None] = mapped_column(index=True)
    ecoPoints: Mapped[float] = mapped_column(default=0.0)
    level: Mapped[int] = mapped_column(default=1)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["RoleOrm"] = relationship(back_populates="users", lazy="joined")
    userStats: Mapped["UserStatsOrm"] = relationship(
        back_populates="users", lazy="joined"
    )
    # deposits: Mapped["DepositOrm"] = relationship(back_populates="users", lazy="joined")
    # reward_redemptions: Mapped["RewardRedemptionOrm"] = relationship(back_populates="users", lazy="joined")  # type: ignore


class RoleOrm(SqlAlchemyBase):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    users: Mapped[list["UserOrm"]] = relationship(
        back_populates="role", lazy="selectin"
    )


class UserStatsOrm(SqlAlchemyBase):
    __tablename__ = "userStats"

    totalDeposits: Mapped[float] = mapped_column(default=0.0)
    plasticKg: Mapped[float] = mapped_column(default=0.0)
    paperKg: Mapped[float] = mapped_column(default=0.0)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped[UserOrm] = relationship(back_populates="userStats", lazy="joined")
