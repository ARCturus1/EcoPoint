from pydantic import BaseModel, Field
import datetime as dt


class UpdateDepositModel(BaseModel):
    user_id: int | None = Field(None)  # Кто сдал
    # users: Mapped[UserOrm] = relationship(back_populates="deposits")
    bin_id: int | None = Field(None)  # Кто сдал
    # bins: Mapped[BinOrm] = relationship(back_populates="deposits")
    waste_type: str | None = Field(None, max_length=20)
    weight_kg: float | None = Field(None)
    eco_points_earned: int | None = Field(None)


class CreateDepositModel(BaseModel):
    user_id: int  # Кто сдал
    # users: Mapped[UserOrm] = relationship(back_populates="deposits")
    bin_id: int  # Кто сдал
    # bins: Mapped[BinOrm] = relationship(back_populates="deposits")
    waste_type: str = Field(max_length=20)
    weight_kg: float = Field(default=0.0)
    eco_points_earned: int = Field(default=0)
    created_at: dt.datetime


class GetDepositModel(BaseModel):
    id: int
    user_id: int | None = Field(None)  # Кто сдал
    # users: Mapped[UserOrm] = relationship(back_populates="deposits")
    bin_id: int | None = Field(None)  # Кто сдал
    # bins: Mapped[BinOrm] = relationship(back_populates="deposits")
    waste_type: str | None = Field(None, max_length=20)
    weight_kg: float | None = Field(None)
    eco_points_earned: int | None = Field(None)
