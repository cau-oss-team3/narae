from fastapi import APIRouter

from .schemas import PingResponseSchema

router = APIRouter(prefix='/healthcheck', tags=['Healthcheck'])


@router.get(
    '/ping/',
    description='Ping healthcheck',
    response_model=PingResponseSchema,
)
async def ping():
    return PingResponseSchema()