import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import auth, matching, analyzer, builds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

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
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response


