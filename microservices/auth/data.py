from common.base.data import BaseRepository
from models import UserOrm
from schemas import (
    RequestCreateUserModel,
    CreateUserModel,
    EditUserModel,
    UserModel,
)


class UserData(BaseRepository[UserOrm, UserModel, CreateUserModel, EditUserModel]):
    model = UserOrm
    schema_response = UserModel
    schema_create = CreateUserModel
    schema_update = EditUserModel
