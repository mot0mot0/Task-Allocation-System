from fastapi import APIRouter, HTTPException
from src.schemas.requests import AllocationRequest, AllocationResponse
from services.task_allocator import TaskAllocator

router = APIRouter()
allocator = TaskAllocator()

@router.post("/allocate", response_model=AllocationResponse)
async def allocate_tasks(request: AllocationRequest):
    try:
        allocation = allocator.allocate_tasks(request.tasks, request.executors)
        return {"allocation": allocation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
