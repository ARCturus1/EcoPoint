from typing import Any
from dataclasses import dataclass

from pydantic import BaseModel, EmailStr, Field, model_validator


class LoginRequestModel(BaseModel):
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", min_length=3
    )
    password: str = Field(..., pattern=r"^[a-zA-Z0-9]+$", min_length=6, max_length=20)


class LoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str


class RefreshModel(BaseModel):
    refresh_token: str


class RegisterRequestModel(BaseModel):
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", min_length=3
    )
    name: str = Field(..., min_length=3)
    password: str = Field(..., pattern=r"^[a-zA-Z0-9]+$", min_length=6, max_length=20)
    confirmPassword: str = Field(
        ..., pattern=r"^[a-zA-Z0-9]+$", min_length=6, max_length=20
    )

    @model_validator(mode="before")
    def passwords_match_validator(cls, data: Any) -> Any:
        if data["password"] != data["confirmPassword"]:
            raise ValueError("Password and Confirm Password must be equals")
        return data


class RegisterResponseModel(BaseModel):
    accessToken: str
    refreshToken: str


@dataclass
class TokenModel:
    """Interface for token response containing access and refresh tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserModel(BaseModel):
    id: int | None = None
    email: EmailStr
    name: str
    hash: str


class RequestCreateUserModel(BaseModel):
    email: EmailStr
    name: str
    hash: str


class CreateUserModel(RequestCreateUserModel):
    role_id: int = 2


class EditUserModel(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


@dataclass
class TokenPayloadData:
    id: str
    email: str
