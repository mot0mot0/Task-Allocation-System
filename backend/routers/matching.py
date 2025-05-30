from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_matching():
    return {"message": "Matching endpoint"}
