import os
import base64

# from authx import AuthX, AuthXConfig, TokenPayload, RequestToken
from passlib.context import CryptContext
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import jwt
from fastapi import Depends
from dotenv import load_dotenv
from datetime import timedelta
from time import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()
security = HTTPBearer()

ISSUER = os.getenv("JWT_ISSUER")
AUDIENCE = os.getenv("AUDIENCE")
EXP = os.getenv("EXP")
EXP_REFRESH = os.getenv("EXP_REFRESH")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# config = AuthXConfig()
# config.JWT_ALGORITHM = "RS256"
# config.JWT_SECRET_KEY = "secret!!!"
# config.JWT_ENCODE_ISSUER = ISSUER
# config.JWT_DECODE_ISSUER = ISSUER
# config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(milliseconds=1800000)
KID = "key-1"  # Идентификатор ключа (важен для ротации ключей)
with open("./keys/private_key.pem", "rt") as reader:
    JWT_PRIVATE_KEY = reader.read()
with open("./keys/public_key.pem", "rt") as reader:
    JWT_PUBLIC_KEY = reader.read()


# security = AuthX(config=config)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_dep = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# def access_token_required(
#     tokenPayload: TokenPayload = Depends(security.access_token_required),
#     token: str = Depends(oauth2_dep),
# ):
#     return tokenPayload


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    if token := credentials.credentials:
        return decode_token(token)
    return {}


def decode_token(token: str) -> dict:
    if JWT_ALGORITHM:
        return jwt.decode(
            token=token,
            key=str(JWT_PRIVATE_KEY),
            algorithms=[JWT_ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
    return {}


def encode_data(src: dict) -> str:
    now_in_seconds = int(time())

    base_dict = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now_in_seconds,
    }

    headers = {"alg": JWT_ALGORITHM, "kid": KID}

    return jwt.encode(
        {**src, **base_dict},
        key=str(JWT_PRIVATE_KEY),
        algorithm=JWT_ALGORITHM or "RS265",
        headers=headers,
    )


def create_access_token(src: dict) -> str:
    now_in_seconds = int(time())
    delta = timedelta(minutes=int(EXP or "15")).total_seconds()

    time_dict = {"exp": int(now_in_seconds + delta)}

    return encode_data({**src, **time_dict})


def create_refresh_token(src: dict) -> str:
    now_in_seconds = int(time())
    delta = timedelta(days=int(EXP_REFRESH or "7")).total_seconds()

    time_dict = {"exp": int(now_in_seconds + delta)}

    return encode_data({**src, **time_dict})


def verify_refresh_token(token: str) -> dict:
    """Verify and decode a refresh token."""
    try:
        return decode_token(token)
    except Exception as e:
        raise ValueError("Invalid refresh token") from e


def get_public_jwk() -> dict:
    """
    Преобразует публичный ключ PEM в формат JWK для JWKS
    """
    with open("./keys/public_key.pem", "rb") as f:
        PUBLIC_KEY = f.read()

    key = serialization.load_pem_public_key(PUBLIC_KEY, backend=default_backend())

    # Получаем числа n (modulus) и e (exponent)
    numbers = key.public_numbers()  # type: ignore

    # Функция для кодирования в Base64URL (стандарт для JWK)
    def int_to_base64url(n: int) -> str:
        # Конвертируем число в байты
        byte_length = (n.bit_length() + 7) // 8
        return (
            base64.urlsafe_b64encode(n.to_bytes(byte_length, "big"))
            .rstrip(b"=")
            .decode("utf-8")
        )

    return {
        "kty": "RSA",
        "use": "sig",
        "kid": KID,
        "alg": JWT_ALGORITHM,
        "n": int_to_base64url(numbers.n),  # type: ignore
        "e": int_to_base64url(numbers.e),  # type: ignore
    }
