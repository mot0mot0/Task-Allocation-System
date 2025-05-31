from services.llm_interface import LlamaModelInterface
from src.pocketbase import Pocketbase
from pathlib import Path
import sys

# Получаем базовую директорию
if getattr(sys, "frozen", False):
    # Если запущено как exe
    base_dir = Path(sys.executable).parent
else:
    # Если запущено как скрипт
    base_dir = Path(__file__).parent.parent

LLAMA_MODEL_PATH = str(
    base_dir / "assets" / "models" / "Mistral-7B-Instruct-v0.3.Q4_K_S.gguf"
)
POCKETBASE_URL = "http://127.0.0.1:8090"

LLAMA_INTERFACE = LlamaModelInterface(model_path=LLAMA_MODEL_PATH)
PB = Pocketbase(POCKETBASE_URL)


class PocketbaseCollections:
    USERS = "users"
    EXECUTORS = "executors"
