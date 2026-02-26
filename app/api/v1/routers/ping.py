from fastapi import APIRouter, status, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from db.models import User, UserRole
from db.shemas import UserID


test_router = APIRouter(prefix='/api/v1/ping', tags=['Test', ])


@test_router.get('/', summary='Test pattern', status_code=status.HTTP_200_OK)
async def pong() -> dict[str, str]:
    return {'message': 'success'}


@test_router.patch('/create-admin', summary='Создание админа роли для теста', status_code=status.HTTP_200_OK)
async def create_admin(user_id: UserID, connection: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id.user_id)
    db_data = await connection.execute(query)
    user = db_data.scalars().one()

    user.role = UserRole.admin

    await connection.commit()

    return {'message': 'success'}
