from services.llm_interface import LlamaModelInterface
from src.pocketbase import Pocketbase

LLAMA_MODEL_PATH = "assets/models/Mistral-7B-Instruct-v0.3.Q4_K_S.gguf"
POCKETBASE_URL = "http://127.0.0.1:8090"

LLAMA_INTERFACE = LlamaModelInterface(model_path=LLAMA_MODEL_PATH)
PB = Pocketbase(POCKETBASE_URL)

# Настройки аутентификации
SECRET_KEY = "your-secret-key"  # В продакшене использовать безопасный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Сообщения об ошибках
ERROR_MESSAGES = {
    "not_found": "Запись не найдена",
    "already_exists": "Запись уже существует",
    "invalid_credentials": "Неверные учетные данные",
    "unauthorized": "Требуется аутентификация",
    "forbidden": "Доступ запрещен",
    "validation_error": "Ошибка валидации данных",
    "database_error": "Ошибка базы данных",
    "server_error": "Внутренняя ошибка сервера",
}


class PocketbaseCollections:
    USERS = "users"
    EXECUTORS = "executors"
