import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Централизованная настройка логирования для всего приложения"""
    # Создаем директорию для логов
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Базовый форматтер для всех логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Настраиваем логгер для бэкенда
    backend_logger = logging.getLogger("backend")
    backend_logger.setLevel(logging.INFO)
    backend_logger.propagate = False
    backend_logger.handlers = []

    backend_handler = RotatingFileHandler(
        log_dir / "backend.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    backend_handler.setFormatter(formatter)
    backend_logger.addHandler(backend_handler)

    # Настраиваем логгер для allocator
    allocator_logger = logging.getLogger("task_allocator")
    allocator_logger.setLevel(logging.INFO)
    allocator_logger.propagate = False
    allocator_logger.handlers = []

    allocator_handler = RotatingFileHandler(
        log_dir / "allocator.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    allocator_handler.setFormatter(formatter)
    allocator_logger.addHandler(allocator_handler)

    # Настраиваем логгер для LLM
    llm_logger = logging.getLogger("llm_interface")
    llm_logger.setLevel(logging.INFO)
    llm_logger.propagate = False
    llm_logger.handlers = []

    llm_handler = RotatingFileHandler(
        log_dir / "llm.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    llm_handler.setFormatter(formatter)
    llm_logger.addHandler(llm_handler)

    # Настраиваем логгер для matching router
    matching_logger = logging.getLogger("matching_router")
    matching_logger.setLevel(logging.INFO)
    matching_logger.propagate = False
    matching_logger.handlers = []

    matching_handler = RotatingFileHandler(
        log_dir / "backend.log",  # Используем тот же файл, что и для бэкенда
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    matching_handler.setFormatter(formatter)
    matching_logger.addHandler(matching_handler)

    # Настраиваем логгеры для uvicorn
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi"]:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.propagate = False
        uvicorn_logger.handlers = []

        uvicorn_handler = RotatingFileHandler(
            log_dir / "backend.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        uvicorn_handler.setFormatter(formatter)
        uvicorn_logger.addHandler(uvicorn_handler)

    # Отключаем все остальные логгеры
    for name in logging.root.manager.loggerDict:
        if name not in ["backend", "task_allocator", "llm_interface", "matching_router", 
                       "uvicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi"]:
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = False 