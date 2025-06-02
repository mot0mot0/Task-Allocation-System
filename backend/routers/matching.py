from fastapi import APIRouter
from fastapi import HTTPException
from src.schemas.requests import AllocationRequest
from services.task_allocator import allocate_tasks

router = APIRouter()


@router.post("/allocate")
async def allocate(request: AllocationRequest):
    try:
        allocation = allocate_tasks(request.tasks, request.executors)
        return {"allocation": allocation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
