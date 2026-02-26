import jwt

from typing import Sequence

from fastapi import APIRouter, status, Depends, exceptions, responses, Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_db
from db.shemas import UserRegistration, Success, UserLogin, User as UserSchema, UserUpdate, UserID
from db.models import User, UserRole
from core import hash_password, verify_password, create_access_token, create_refresh_token, settings
from utils import get_user, get_admin


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

    print('~~~~~~~~~~~~ID~~~~~~~~~~~~', user.id, '~~~~~~~~~~~~ID~~~~~~~~~~~~', sep='\n')

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
        secure=False,  # TODO True на проде
        path='/user/refresh'
    )

    return response


@user_router.post('/refresh', summary='Обновление access токена', status_code=status.HTTP_202_ACCEPTED)
async def refresh(request: Request):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(refresh_token, settings.ACCESS_TOKEN_KEY, settings.ALGORITHM)
    except Exception:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    if payload.get('type') != 'refresh':
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_401_UNAUTHORIZED)

    encode_data = {'sub': payload['sub']}
    new_access = create_access_token(encode_data)

    return {'message': f'{new_access}'}


@user_router.post('/logout', summary='Выход из системы', status_code=status.HTTP_200_OK)
async def logout():
    response = responses.Response(status_code=204)
    response.delete_cookie('refresh_token', path='/user/refresh')
    return response


@user_router.get('/detail', summary='Детальная информация', status_code=status.HTTP_202_ACCEPTED)
async def get_detail(current_user: User = Depends(get_user)) -> UserSchema:
    return current_user


@user_router.delete('/delete', summary='Удаление', status_code=status.HTTP_200_OK)
async def delete_user(current_user: User = Depends(get_user), connection: AsyncSession = Depends(get_db)):
    current_user.is_deleted = True

    await connection.commit()
    await connection.refresh(current_user)

    return {'message': 'success'}


@user_router.patch('/detail/update', summary='Изменение профиля', status_code=status.HTTP_202_ACCEPTED)
async def user_update(data: UserUpdate, current_user: User = Depends(get_user), connection: AsyncSession = Depends(get_db)):
    data = data.model_dump(exclude_unset=True)

    if not data:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_400_BAD_REQUEST)

    for field, value in data.items():
        setattr(current_user, field, value)

    await connection.commit()
    await connection.refresh(current_user)

    return {'message': 'success'}


@user_router.get('/admin/show-all', summary='Получение списка всех пользователей', status_code=status.HTTP_200_OK)
async def show_all_users(admin: User = Depends(get_admin), connection: AsyncSession = Depends(get_db)) -> Sequence[UserSchema]:

    query = select(User)
    db_data = await connection.execute(query)
    users = db_data.scalars().all()

    return users


@user_router.patch('/admin/user-up', summary='Повышение пользователя до админа', status_code=status.HTTP_200_OK)
async def user_up(user_id: UserID, admin: User = Depends(get_admin), connection: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id.user_id)
    db_data = await connection.execute(query)
    user = db_data.scalar_one_or_none()

    if not user:
        raise exceptions.HTTPException(detail='Error', status_code=status.HTTP_400_BAD_REQUEST)

    user.role = UserRole.admin

    await connection.commit()
    await connection.refresh(user)

    return {'message': 'success'}
