import json
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime

from src.constants import LLAMA_INTERFACE
from src.schemas.responses import ResponseTemplate
from src.schemas.requests import TasksData, ExecutorData, SingleTaskData, TaskAnalysisRequest, ExecutorAnalysisRequest, TaskWithSkills, ExecutorWithSkills
from services.llm_analyzer import LLMAnalyzer


router = APIRouter()
analyzer = LLMAnalyzer()


@router.post(
    "/tasks",
    tags=["analyzer"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "id": "task_id",
                            "title": "task_title",
                            "assessment": {
                                "soft": {"skill1": "number", "skill2": "number"},
                                "hard": {"skill3": "number", "skill4": "number"},
                            },
                        },
                    },
                },
            },
        ]
    ).create_response(),
)
async def analyze_tasks(data: TasksData):
    try:
        try:
            json.dumps(data.model_dump(), ensure_ascii=False)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

        async def generate():
            try:
                task_list = [task.model_dump() for task in data.task_list]

                for result in LLAMA_INTERFACE.analyze_tasks(
                    data.project_description, task_list
                ):
                    yield json.dumps(result, ensure_ascii=False)
            except Exception as e:
                error_response = {"error": str(e), "status": "error"}
                yield json.dumps(error_response, ensure_ascii=False)

        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/executor",
    tags=["analyzer"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "name": "executor_name",
                            "assessment": {
                                "soft": {"skill1": "number", "skill2": "number"},
                                "hard": {"skill3": "number", "skill4": "number"},
                            },
                        },
                    },
                },
            },
        ]
    ).create_response(),
)
async def analyze_executor(data: ExecutorData):
    try:
        result = LLAMA_INTERFACE.analyze_executor(data.resume)
        result["name"] = data.name
        result["id"] = data.id

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/task",
    tags=["analyzer"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "id": "task_id",
                            "title": "task_title",
                            "assessment": {
                                "soft": {"skill1": "number", "skill2": "number"},
                                "hard": {"skill3": "number", "skill4": "number"},
                            },
                        },
                    },
                },
            },
        ]
    ).create_response(),
)
async def analyze_single_task(data: SingleTaskData):
    try:
        try:
            json.dumps(data.model_dump(), ensure_ascii=False)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

        # Создаем список из одной задачи
        task_list = [data.model_dump()]

        # Получаем результат анализа
        result = next(
            LLAMA_INTERFACE.analyze_tasks(data.project_description, task_list)
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/task")
async def analyze_task(request: TaskAnalysisRequest):
    try:
        # Преобразуем строки дат в datetime
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)
        
        # Проверяем корректность дат
        if end_date <= start_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
            
        assessment = await analyzer.analyze_task(
            request.task,
            start_date,
            end_date
        )
        return {"assessment": assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/executor")
async def analyze_executor(request: ExecutorAnalysisRequest):
    try:
        assessment = await analyzer.analyze_executor(request.executor)
        return {"assessment": assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
