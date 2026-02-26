from fastapi import APIRouter, status, Depends, exceptions, responses

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_db
from db.shemas import UserRegistration, Success, UserLogin, JWTTokens
from db.models import User
from core import hash_password, verify_password, create_access_token, create_refresh_token


user_router = APIRouter(prefix='/user', tags=['Пользователь', ])


@user_router.post('/registration', summary='Регистрация', status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, connection: AsyncSession = Depends(get_db)):
    pwd_1 = data.password
    pwd_2 = data.accept_password

    if pwd_1 != pwd_2:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_400_BAD_REQUEST)

    pwd_hash = hash_password(password=pwd_1)

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        surname=data.surname,
        email=data.email,
        password_hash=pwd_hash
    )

    connection.add(user)

    try:
        await connection.commit()
    except Exception:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    await connection.refresh(user)

    return Success()


@user_router.post('/login', summary='Вход', status_code=status.HTTP_202_ACCEPTED)
async def login(data: UserLogin, connection: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == data.email)
    try:
        db_data = await connection.execute(query)
    except Exception:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    user = db_data.scalar_one_or_none()  # TODO Выше можно перенести в отдельную функцию

    if user is None:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(user.password_hash, data.password):
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    encode_data = {'sub': str(user.id)}

    access_token = create_access_token(encode_data)
    refresh_token = create_refresh_token(encode_data)

    print(refresh_token)  # TODO можно будет удалить, для дальнейших тестов понадобится

    response = responses.JSONResponse(content={'access_token': access_token})

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        path='/refresh'
    )

    return response
