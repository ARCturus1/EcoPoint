import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import Request
from jose import JWSError

# from ...common.base.data import BaseRepository
from common import BaseRepository
from common.base.service import BaseService
from data import UserData
from models import UserOrm
from schemas import (
    RequestCreateUserModel,
    CreateUserModel,
    EditUserModel,
    TokenModel,
    UserModel,
)
from database import get_async_alchemy_session
from utils import (
    get_public_jwk,
    pwd_context,
    decode_token,
    create_access_token,
    create_refresh_token,
)
from dotenv import load_dotenv

load_dotenv()
AUDIENCE = os.getenv("AUDIENCE")


class AuthService(BaseService[UserModel, CreateUserModel, EditUserModel, UserOrm]):
    dataCrud: BaseRepository[UserOrm, UserModel, CreateUserModel, EditUserModel]

    def __init__(self) -> None:
        self.dataCrud = UserData(get_async_alchemy_session)
        super().__init__()

    schema_response = UserModel
    schema_create = CreateUserModel
    schema_update = EditUserModel

    async def create(self, obj_in: CreateUserModel) -> UserModel | None:
        obj_in.hash = pwd_context.hash(obj_in.hash)
        obj_in.role_id = 2
        return await super().create(obj_in)

    async def lookup_user(self, **filters) -> UserModel | None:
        if user := await self.get_one(**filters):
            return user

        return None

    async def auth_user(self, email: str, plain: str) -> UserModel | None:
        if not (user := await self.lookup_user(email=email)):
            return None

        if not self.__verify_password(plain, user.hash):
            return None

        return user

    def create_tokens_pair(
        self, email: str, data: dict | None = None
    ) -> TokenModel | None:
        if not email:
            return None

        # access_token = security.create_access_token(
        #     uid=email, data=data, audience=AUDIENCE
        # )
        access_token = create_access_token({"sub": email})
        refresh_token = create_refresh_token({"sub": email})

        return TokenModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_current_user(
        self, token: str | None = None, email: str | None = None
    ) -> UserModel | None:
        if not email:
            if token and not (email := self.get_jwt_username(token)):
                return None

        if user := await self.lookup_user(email=email):
            return user

        return None

    def get_jwt_username(self, token: str) -> str | None:
        try:
            # breakpoint()
            payload = decode_token(token)

            # payload = security._decode_token(token=token)
            # con = payload1.decode(token=token, key="sub")
            # breakpoint()
            if not (email := payload.get("sub")):
                # if not (email := payload.sub):
                return None
        except JWSError:
            return None

        return email

    async def refresh_token_required(self, request: Request) -> dict:
        """Verify refresh token from request headers."""
        from fastapi import HTTPException

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Invalid or missing refresh token"
            )

        token = auth_header.split(" ")[1]
        try:
            payload = decode_token(token)
            return payload
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    #     # --- Хелпер для конвертации PEM в JWK ---

    def get_public_jwks(self) -> dict:
        return get_public_jwk()

    # def verify_refresh_token(self, token: str) -> TokenPayload:
    #     """Verify refresh token manually."""
    #     return security.verify_token(
    #         token=RequestToken(token=token, type="refresh", location="headers")
    #     )

    def __verify_password(self, plain: str, hash: str) -> bool:
        return pwd_context.verify(plain, hash)
