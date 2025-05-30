import sys
import subprocess
import signal
import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import socket
import re
import requests
from tqdm import tqdm

# Setting up logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

startup_handler = RotatingFileHandler(
    log_dir / "startup.log",
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5,
    encoding="utf-8",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[startup_handler, logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


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
    pocketbase_dir = Path(__file__).parent.parent.parent / "pocketbase"
    pocketbase_dir.mkdir(parents=True, exist_ok=True)

    pocketbase_exe = pocketbase_dir / "pocketbase.exe"
    pocketbase_url = "https://github.com/pocketbase/pocketbase/releases/download/v0.22.4/pocketbase_0.22.4_windows_amd64.zip"

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
        # Extract archive
        import zipfile

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
    model_dir = Path(__file__).parent.parent / "assets" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "Mistral-7B-Instruct-v0.3.Q4_K_S.gguf"
    model_url = "https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3.Q4_K_S.gguf"

    if model_path.exists():
        logger.info("LLM model found")
        return True

    logger.info("LLM model not found, downloading...")
    if download_file(model_url, model_path):
        logger.info("LLM model downloaded successfully")
        return True
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
        self.base_dir = Path(__file__).parent.parent.absolute()
        self.pocketbase_dir = self.base_dir.parent / "pocketbase"
        self.pocketbase_exe = self.pocketbase_dir / "pocketbase.exe"
        self.pocketbase_port = 8090
        self.backend_port = 8000

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

    def start_backend(self) -> subprocess.Popen | None:
        try:
            if is_port_in_use(self.backend_port):
                logger.error(f"Port {self.backend_port} is already in use")
                return None

            logger.info("Starting FastAPI backend...")
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(self.backend_port),
                ],
                cwd=str(self.base_dir),
                stdout=open(log_dir / "backend.log", "w"),
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.processes.append(process)
            return process
        except Exception as e:
            logger.error(f"Error starting backend: {e}")
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
        print("\nServices started successfully:")
        print(f"├─ Database UI:      http://localhost:{self.pocketbase_port}/_/")
        print(f"├─ Backend API:      http://localhost:{self.backend_port}")
        print(f"└─ Backend DOC:      http://localhost:{self.backend_port}/docs\n")

        # Print superuser URL if available
        pocketbase_log = read_log_file(log_dir / "pocketbase.log")
        superuser_url = extract_superuser_url(pocketbase_log)
        if superuser_url:
            print("Create your first superuser account:")
            print(f"{superuser_url}\n")


def main():
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
        time.sleep(5)

        # Starting backend
        backend_process = manager.start_backend()
        if not backend_process:
            logger.error("Failed to start backend")
            manager.stop_all()
            return

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
