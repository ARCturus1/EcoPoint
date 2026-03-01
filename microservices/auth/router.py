from pathlib import Path
import sys

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from schemas import (
    CreateUserModel,
    EditUserModel,
    LoginRequestModel,
    LoginResponseModel,
    RefreshModel,
    RegisterRequestModel,
    UserModel,
    TokenPayloadData,
)
from service import AuthService
from utils import get_token_payload, verify_refresh_token

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.errors import DuplicateException, MissingException

router = APIRouter(prefix="/api/auth", tags=["Auth"])

crudService = AuthService()


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authentificate": "Bearer"},
    )


@router.get("/health")
def health():
    return {"status": "OK"}


@router.get("")
async def index() -> dict[str, list[UserModel] | int]:
    # return await service.get_all()
    users = await crudService.get_all()
    return {"users": users, "count": len(users)}


@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginResponseModel | None:
    user = await crudService.auth_user(form_data.username, form_data.password)

    if not user:
        unauthed()
        return None

    token_pair = crudService.create_tokens_pair(
        TokenPayloadData(id=str(user.id or 0), email=user.email)
    )

    if token_pair:
        return LoginResponseModel(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
    else:
        return None


@router.get("/get_user/{email}")
async def get_current_user(email: str) -> UserModel | None:
    try:
        return await crudService.get_one(email=email)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("/register", response_model=UserModel)
async def register(body: RegisterRequestModel = Body(None)) -> UserModel | None:
    if not body:
        raise HTTPException(status_code=400, detail="Bad request")

    user = CreateUserModel(email=body.email, name=body.name, hash=body.password)
    try:
        return await crudService.create(user)
    except DuplicateException as exc:
        raise HTTPException(status_code=409, detail=exc.message)

    # return RegisterResponseModel(accessToken="accessToken", refrrefresh_token_requiredeshToken="refreshToken")


@router.patch("/{email}", response_model=UserModel)
async def update_user(
    email: str,
    user: EditUserModel = Body(),
) -> UserModel | None:
    try:
        return await crudService.modify(user, email=email)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/delete/{email}")
async def delete(
    email: str,
) -> None:
    try:
        await crudService.delete(email=email)
    except MissingException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("/refresh", response_model=LoginResponseModel)
async def refresh(
    request: Request, refresh: RefreshModel = Body(None)
) -> LoginResponseModel:
    try:
        # Try to get refresh token from Authorization header first
        refresh_payload = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                refresh_payload = await crudService.refresh_token_required(request)
            except Exception:
                # If header token fails, try body token
                if refresh and refresh.refresh_token:
                    token = refresh.refresh_token
                    refresh_payload = verify_refresh_token(token)
        elif refresh and refresh.refresh_token:
            # Use token from request body
            token = refresh.refresh_token
            refresh_payload = verify_refresh_token(token)

        if not refresh_payload:
            raise HTTPException(
                status_code=401, detail="Invalid or missing refresh token"
            )

        # Create new token pair
        token_pair = crudService.create_tokens_pair(
            TokenPayloadData(id=refresh_payload["id"], email=refresh_payload["email"])
        )

        if token_pair:
            return LoginResponseModel(
                access_token=token_pair.access_token,
                refresh_token=token_pair.refresh_token,
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create tokens")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/login", response_model=LoginResponseModel)
async def login(body: LoginRequestModel = Body()) -> LoginResponseModel | None:
    user = await crudService.auth_user(body.email, body.password)

    if not user:
        unauthed()
        return None

    token_pair = crudService.create_tokens_pair(
        TokenPayloadData(id=str(user.id or 0), email=user.email)
    )

    if token_pair:
        return LoginResponseModel(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
    else:
        return None


@router.get("/.well-known/jwks.json")
async def get_jwks():
    # import json

    # jwk = crudService.get_public_jwks()
    # response_data = {"keys": [jwk]}

    # # ✅ Логируем для проверки
    # print(f"JWKS Response: {json.dumps(response_data)}")

    # return response_data
    return {"keys": [crudService.get_public_jwks()]}
