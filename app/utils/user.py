import jwt

from fastapi import Depends, status, exceptions
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core import settings
from db.models import User
from db import get_db


security = HTTPBearer()


async def get_user(cred: HTTPAuthorizationCredentials = Depends(security), connection: AsyncSession = Depends(get_db)):
    access_token = cred.credentials

    try:
        payload = jwt.decode(access_token, settings.ACCESS_TOKEN_KEY, settings.ALGORITHM)
    except Exception:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_402_UNAUTHORIZED)

    if payload.get('type') is not None:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = payload['sub']

    query = select(User).where(User.id == user_id)
    db_data = await connection.execute(query)
    user = db_data.scalar_one_or_none()

    if user is None:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_400_BAD_REQUEST)

    return user
