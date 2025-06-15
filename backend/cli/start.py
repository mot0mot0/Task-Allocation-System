import sys
import subprocess
import signal
import time
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import socket
import re
import requests
from tqdm import tqdm
import argparse
import uvicorn
import threading
import zipfile


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        # Если запущено как exe
        return Path(sys.executable).parent
    else:
        # Если запущено как скрипт
        return Path(__file__).parent.parent


def clear_log_files():
    log_dir = get_base_dir() / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_files = [
        "startup.log",
        "backend.log",
        "pocketbase.log",
        "llm.log",
        "allocator.log",
        "build.log"
    ]
    
    for log_file in log_files:
        log_path = log_dir / log_file
        if log_path.exists():
            try:
                log_path.unlink()
            except Exception as e:
                print(f"Error clearing log file {log_file}: {e}")


# Setting up logging
base_dir = get_base_dir()
log_dir = base_dir / "logs"
log_dir.mkdir(exist_ok=True)

# Очищаем логи при запуске
clear_log_files()

# Добавляем директорию llama_cpp DLLs для поиска
if getattr(sys, "frozen", False):
    llama_cpp_dll_dir = base_dir / "_internal" / "llama_cpp" / "lib"
    if llama_cpp_dll_dir.exists():
        os.add_dll_directory(str(llama_cpp_dll_dir))
        print(f"Added DLL directory: {llama_cpp_dll_dir}")

# Настраиваем форматтер для логов
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Настраиваем обработчик файла для startup.log
startup_file_handler = RotatingFileHandler(
    log_dir / "startup.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",  # 10MB
)
startup_file_handler.setFormatter(log_formatter)

# Настраиваем обработчик консоли
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# Настраиваем логгер для startup
logger = logging.getLogger("startup")
logger.setLevel(logging.INFO)
logger.addHandler(startup_file_handler)
logger.addHandler(console_handler)

# Настраиваем основной логгер для вывода важных сообщений в консоль
main_logger = logging.getLogger("__main__")
main_logger.setLevel(logging.INFO)
main_logger.addHandler(console_handler)
main_logger.propagate = False

# Отключаем вывод логов в консоль для всех остальных логгеров
for name in logging.root.manager.loggerDict:
    if name != "startup":  # Оставляем только startup логгер
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = False


def download_file(url: str, destination: Path) -> bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte

        with open(destination, "wb") as file, tqdm(
            desc=destination.name,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                bar.update(size)
        return True
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        if destination.exists():
            destination.unlink()
        return False


def check_and_download_pocketbase() -> bool:
    # Determine the path to PocketBase depending on the execution method
    if getattr(sys, "frozen", False):
        # If running as an exe
        pocketbase_dir = base_dir / "pocketbase"
    else:
        # If running as a script
        pocketbase_dir = base_dir.parent / "pocketbase"

    pocketbase_dir.mkdir(parents=True, exist_ok=True)

    pocketbase_exe = pocketbase_dir / "pocketbase.exe"
    current_version = "0.22.4"
    pocketbase_url = f"https://github.com/pocketbase/pocketbase/releases/download/v{current_version}/pocketbase_{current_version}_windows_amd64.zip"

    # Check if PocketBase exists
    if pocketbase_exe.exists():
        logger.info("PocketBase found")
        return True

    logger.info("PocketBase not found, downloading...")

    # Download zip archive
    zip_path = pocketbase_dir / "pocketbase.zip"
    if not download_file(pocketbase_url, zip_path):
        logger.error("Failed to download PocketBase")
        return False

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(pocketbase_dir)

        # Delete zip file
        zip_path.unlink()

        logger.info("PocketBase downloaded and extracted successfully")
        return True
    except Exception as e:
        logger.error(f"Error extracting PocketBase: {e}")
        if zip_path.exists():
            zip_path.unlink()
        return False


def check_and_download_model() -> bool:
    model_dir = base_dir / "assets" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "Mistral-7B-Instruct-v0.3.Q4_K_S.gguf"
    current_version = "v0.3.Q4_K_S"
    model_url = f"https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-{current_version}.gguf"

    # Checking the file size
    if model_path.exists():
        try:
            size_mb = model_path.stat().st_size / (1024 * 1024)
            if size_mb < 1000:  # If less than 1GB, consider file corrupted
                logger.warning(
                    f"Model file seems to be corrupted (size: {size_mb:.2f}MB), downloading again..."
                )
                model_path.unlink()
            else:
                logger.info(f"LLM model found (size: {size_mb:.2f}MB)")
                return True
        except Exception as e:
            logger.error(f"Error checking model file: {e}")
            model_path.unlink()

    logger.info("LLM model not found, downloading...")
    if download_file(model_url, model_path):
        # Checking the file size
        try:
            size_mb = model_path.stat().st_size / (1024 * 1024)
            if size_mb < 1000:
                logger.error(
                    f"Downloaded model file seems to be corrupted (size: {size_mb:.2f}MB)"
                )
                model_path.unlink()
                return False
            logger.info(f"LLM model downloaded successfully (size: {size_mb:.2f}MB)")
            return True
        except Exception as e:
            logger.error(f"Error checking downloaded model: {e}")
            model_path.unlink()
            return False
    else:
        logger.error("Failed to download LLM model")
        return False


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def read_log_file(filename: Path) -> str:
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return f"Failed to read log: {e}"


def extract_superuser_url(log_content: str) -> str:
    pattern = r"http://127\.0\.0\.1:8090/_/#/pbinstal/[^\s]+"
    match = re.search(pattern, log_content)
    return match.group(0) if match else ""


class ServiceManager:
    def __init__(self):
        self.processes = []
        self.base_dir = base_dir
        # Determine the path to PocketBase depending on the execution method
        if getattr(sys, "frozen", False):
            # If running as an exe
            self.pocketbase_dir = self.base_dir / "pocketbase"
        else:
            # If running as a script
            self.pocketbase_dir = self.base_dir.parent / "pocketbase"
        self.pocketbase_exe = self.pocketbase_dir / "pocketbase.exe"
        self.pocketbase_port = 8090
        self.backend_port = 8000
        self.frontend_port = 5173

    def start_pocketbase(self) -> subprocess.Popen | None:
        try:
            if not self.pocketbase_exe.exists():
                logger.error(f"PocketBase not found in {self.pocketbase_exe}")
                return None

            if is_port_in_use(self.pocketbase_port):
                logger.error(f"Port {self.pocketbase_port} is already in use")
                return None

            logger.info("Starting PocketBase...")
            process = subprocess.Popen(
                [str(self.pocketbase_exe), "serve"],
                cwd=str(self.pocketbase_dir),
                stdout=open(log_dir / "pocketbase.log", "w"),
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.processes.append(process)
            return process
        except Exception as e:
            logger.error(f"Error starting PocketBase: {e}")
            return None

    def wait_for_pocketbase(self, timeout: int = 30) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            if is_port_in_use(self.pocketbase_port):
                return True
            time.sleep(0.5)
        return False

    def start_backend(self) -> subprocess.Popen | None:
        try:
            if is_port_in_use(self.backend_port):
                logger.error(f"Port {self.backend_port} is already in use")
                return None

            logger.info("Starting FastAPI backend...")

            def run_uvicorn():
                try:
                    # Определяем путь к main.py в зависимости от способа запуска
                    if getattr(sys, "frozen", False):
                        main_path = (
                            Path(sys.executable).parent / "_internal" / "main.py"
                        )
                        # Добавляем _internal в sys.path
                        sys.path.insert(0, str(main_path.parent))
                    else:
                        main_path = Path(__file__).parent.parent / "main.py"
                        sys.path.insert(0, str(main_path.parent))

                    # Проверяем существование файла
                    if not main_path.exists():
                        main_logger.error(f"main.py not found at: {main_path}")
                        return

                    # Настраиваем логирование Uvicorn
                    uvicorn_logger = logging.getLogger("uvicorn")
                    uvicorn_logger.handlers.clear()  # Удаляем все существующие обработчики
                    uvicorn_file_handler = RotatingFileHandler(
                        log_dir / "backend.log",
                        maxBytes=10 * 1024 * 1024,  # 10MB
                        backupCount=5,
                        encoding="utf-8",
                    )
                    uvicorn_file_handler.setFormatter(
                        logging.Formatter(
                            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                        )
                    )
                    uvicorn_logger.addHandler(uvicorn_file_handler)
                    uvicorn_logger.setLevel(logging.INFO)
                    uvicorn_logger.propagate = False  # Отключаем распространение логов

                    # Настраиваем логирование для всех остальных логгеров
                    for name in ["uvicorn.error", "uvicorn.access", "uvicorn.asgi", "fastapi"]:
                        log = logging.getLogger(name)
                        log.handlers.clear()
                        log.addHandler(uvicorn_file_handler)
                        log.setLevel(logging.INFO)
                        log.propagate = False

                    # Запускаем uvicorn
                    uvicorn.run(
                        "main:app",
                        host="127.0.0.1",
                        port=self.backend_port,
                        log_level="info",
                        log_config=None,  # Отключаем дефолтную конфигурацию Uvicorn
                        access_log=True,  # Включаем логирование доступа
                    )
                except Exception as e:
                    logger.error(f"Error in run_uvicorn: {e}", exc_info=True)

            # Запускаем uvicorn в отдельном потоке
            backend_thread = threading.Thread(target=run_uvicorn)
            backend_thread.daemon = True
            backend_thread.start()

            # Создаем фиктивный процесс для отслеживания состояния
            class DummyProcess:
                def __init__(self):
                    self._returncode = None
                    self.stdout = open(log_dir / "backend.log", "w")
                    self.stderr = self.stdout

                def poll(self):
                    return self._returncode

                def wait(self, timeout=None):
                    return 0

                def terminate(self):
                    pass

                def kill(self):
                    pass

            process = DummyProcess()
            self.processes.append(process)
            return process

        except Exception as e:
            logger.error(f"Error starting backend: {e}", exc_info=True)
            return None

    def stop_all(self):
        logger.info("Stopping all services...")
        for process in self.processes:
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                logger.error(f"Error stopping process: {e}")
                try:
                    process.kill()
                except:
                    pass

    def print_service_urls(self):
        # Используем print вместо logger для вывода URL в консоль
        print("\nServices started successfully:")
        print(f"├─ Application UI:   http://localhost:{self.frontend_port}")
        print(f"├─ Database UI:      http://localhost:{self.pocketbase_port}/_/")
        print(f"├─ Backend API:      http://localhost:{self.backend_port}")
        print(f"└─ Backend DOC:      http://localhost:{self.backend_port}/docs\n")

        # Print superuser URL if available
        pocketbase_log = read_log_file(log_dir / "pocketbase.log")
        superuser_url = extract_superuser_url(pocketbase_log)
        if superuser_url:
            print("Create your first superuser account:")
            print(f"{superuser_url}\n")


def install_dependencies():
    try:
        # Set environment variables for building llama-cpp-python
        os.environ["CMAKE_ARGS"] = (
            "-DGGML_AVX2=ON -DGGML_FMA=ON -DGGML_F16C=ON -DGGML_OPENMP=ON"
        )

        # Install dependencies
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )
        logger.info("Dependencies installed successfully")
        return True
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Task Allocation System")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--logs", action="store_true", help="View logs")
    parser.add_argument(
        "--type",
        type=str,
        help="Type of logs to view (backend, llm, pocketbase, startup)",
    )
    parser.add_argument("--tail", type=int, help="Show last N lines of log")
    parser.add_argument("--since", type=int, help="Show logs for the last N hours")

    args = parser.parse_args()

    if args.install:
        if not install_dependencies():
            return

    if args.logs:
        from logs import view_logs

        view_logs(args)
        return

    # Check and download PocketBase
    if not check_and_download_pocketbase():
        logger.error("Failed to prepare PocketBase, exiting...")
        return

    # Check and download LLM model
    if not check_and_download_model():
        logger.error("Failed to prepare LLM model, exiting...")
        return

    manager = ServiceManager()
    should_exit = False

    def signal_handler(signum, frame):
        nonlocal should_exit
        logger.info("Received termination signal")
        should_exit = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Starting PocketBase
        pocketbase_process = manager.start_pocketbase()
        if not pocketbase_process:
            logger.error("Failed to start PocketBase")
            return

        # Waiting for PocketBase to start
        if not manager.wait_for_pocketbase():
            logger.error("Failed to wait for PocketBase to start")
            manager.stop_all()
            return

        # Starting backend
        backend_process = manager.start_backend()
        if not backend_process:
            logger.error("Failed to start backend")
            manager.stop_all()
            return
        
        logger.info("Starting frontend...")

        # Show URLs
        manager.print_service_urls()

        # Waiting for completion
        while not should_exit:
            time.sleep(1)
            if (
                pocketbase_process.poll() is not None
                or backend_process.poll() is not None
            ):
                break

    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if not should_exit:  # Only stop if not already stopping
            manager.stop_all()


if __name__ == "__main__":
    main()
