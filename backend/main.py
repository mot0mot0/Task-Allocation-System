import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.logger import setup_logging

from routers import auth, matching, analyzer, builds

# Настраиваем логирование
setup_logging()

# Получаем логгер для бэкенда
logger = logging.getLogger("backend")

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(matching.router, prefix="/match", tags=["matching"])
app.include_router(analyzer.router, prefix="/analyze", tags=["analyzer"])
app.include_router(builds.router, prefix="/build", tags=["builds"])

@app.get("/")
async def health_check():
    return JSONResponse(
        content={
            "status": "ok",
            "message": "Service is running",
            "version": "1.0.0"
        },
        status_code=200
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {request.method} {request.url} - Status: {response.status_code}")
    return response


