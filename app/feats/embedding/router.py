from fastapi import APIRouter


router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.get(
    "/embedding/",
    description="Test embedding",
)
async def embedding():
    return {"message": "Test embedding"}
