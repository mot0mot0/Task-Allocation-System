import logging
from fastapi import APIRouter, HTTPException
from src.logger import setup_logging
from services.task_allocator import TaskAllocator
from src.schemas.requests import AllocationRequest, AllocationResponse

# Настраиваем логирование
setup_logging()

# Получаем логгер для matching router
logger = logging.getLogger("matching_router")

router = APIRouter()
task_allocator = TaskAllocator()

@router.post("/allocate", response_model=AllocationResponse)
async def allocate_tasks(data: AllocationRequest):
    try:
        logger.info(f"Received allocation request for {len(data.tasks)} tasks and {len(data.executors)} executors")
        
        if not data.tasks or not data.executors:
            logger.warning("Empty tasks or executors list received")
            raise HTTPException(status_code=400, detail="Tasks and executors lists cannot be empty")
        
        # Распределяем задачи
        allocation = task_allocator.allocate_tasks(data.tasks, data.executors)
        
        # Преобразуем результат в формат, ожидаемый фронтендом
        result = {}
        for executor_id, tasks in allocation.items():
            for task in tasks:
                result[task.id] = executor_id
        
        logger.info("Task allocation completed successfully")
        return {"allocation": result}
        
    except Exception as e:
        logger.error(f"Error during task allocation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
