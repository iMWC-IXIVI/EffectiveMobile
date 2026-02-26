import jwt

from datetime import datetime, timedelta

from argon2 import PasswordHasher, exceptions

from core import settings


pwd_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Создание хэша пароля"""
    return pwd_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Проверка пароля на валидность"""
    try:
        pwd_hasher.verify(password_hash, password)
        return True
    except exceptions.VerifyMismatchError:
        return False


def create_access_token(encode_data: dict) -> str:
    """Создание access токена"""
    exp = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data['exp'] = exp
    access_token = jwt.encode(payload=encode_data, key=settings.ACCESS_TOKEN_KEY, algorithm=settings.ALGORITHM)

    return access_token


def create_refresh_token(encode_data: dict) -> str:
    """Создание refresh токена"""
    exp = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    encode_data['exp'] = exp
    encode_data['type'] = 'refresh'

    refresh_token = jwt.encode(payload=encode_data, key=settings.ACCESS_TOKEN_KEY, algorithm=settings.ALGORITHM)
    return refresh_token
