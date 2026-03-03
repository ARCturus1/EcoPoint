from typing import Any

from common.base.data import BaseRepository
from models import UserOrm
from schemas import (
    RequestCreateUserModel,
    CreateUserModel,
    EditUserModel,
    UserModel,
)


class UserData(BaseRepository[UserOrm, UserModel, CreateUserModel, EditUserModel]):
    def __init__(self, database_name: str, **kwargs: Any) -> None:
        super().__init__(database_name, **kwargs)
        self.model = UserOrm
        self.schema_response = UserModel
        self.schema_create = CreateUserModel
        self.schema_update = EditUserModel
