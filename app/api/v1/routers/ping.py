from fastapi import APIRouter, status


test_router = APIRouter(prefix='/api/v1/ping', tags=['Test', ])


@test_router.get('/', summary='Test pattern', status_code=status.HTTP_200_OK)
async def pong() -> dict[str, str]:
    return {'message': 'success'}
