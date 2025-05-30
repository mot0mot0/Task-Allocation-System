import json
import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from src.constants import LLAMA_INTERFACE
from src.schemas.responses import ResponseTemplate
from src.schemas.requests import TasksData, ExecutorData


router = APIRouter()
logger = logging.getLogger(__name__)


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
async def analyze_tasks(request: Request):
    try:
        raw_data = await request.json()
        logger.info(f"Raw request data: {json.dumps(raw_data, ensure_ascii=False)}")

        try:
            data = TasksData(**raw_data)
            logger.info(
                f"Validated data: {json.dumps(data.model_dump(), ensure_ascii=False)}"
            )
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

        async def generate():
            try:
                task_list = [task.model_dump() for task in data.task_list]

                for result in LLAMA_INTERFACE.analyze_tasks(
                    data.project_description, task_list
                ):
                    yield json.dumps(result, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Error in generate: {str(e)}")
                error_response = {"error": str(e), "status": "error"}
                yield json.dumps(error_response, ensure_ascii=False)

        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson",
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
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
        logger.info(f"Analyzing executor: {data.name}")

        result = LLAMA_INTERFACE.analyze_executor(data.resume)
        result["name"] = data.name

        return result

    except Exception as e:
        logger.error(f"Error analyzing executor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
