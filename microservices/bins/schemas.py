from decimal import Decimal
from pydantic import BaseModel, Field
import datetime as dt

# from typing import Optional


class UpdateBinModel(BaseModel):
    name: str | None = Field(None, max_length=100)
    qr_code: str | None = Field(None, max_length=100)
    address: str | None = Field(None)
    lat: Decimal | None = Field(None, max_digits=9, decimal_places=6)
    lng: Decimal | None = Field(None, max_digits=9, decimal_places=6)
    accepted_waste_types: str | None = Field(None)
    is_active: bool | None = Field(None)


class CreateBinModel(BaseModel):
    name: str = Field(max_length=100)
    qr_code: str = Field(max_length=100)
    address: str
    lat: Decimal = Field(max_digits=9, decimal_places=6)
    lng: Decimal = Field(max_digits=9, decimal_places=6)
    accepted_waste_types: str
    is_active: bool = False
    installed_at: dt.datetime


class GetBinModel(UpdateBinModel):
    id: int
