import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import auth, matching, analyzer

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = FastAPI(
    title="Task Allocation System",
    description="Backend API для системы распределения задач",
    version="1.0.0",
)

origins = ["http://localhost:5000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(matching.router, prefix="/matching", tags=["matching"])
app.include_router(analyzer.router, prefix="/analyze", tags=["analyzer"])


@app.middleware("http")
async def block_root_requests(request: Request, call_next):
    if request.url.path == "/":
        return JSONResponse(
            status_code=200,
            content={
                "message": "Welcome to Task Allocation System API",
                "version": "1.0.0",
                "documentation": "/docs",
                "status": "success",
            },
        )
    response = await call_next(request)
    return response
