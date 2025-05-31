import os
from pathlib import Path
import PyInstaller.__main__
import shutil
import datetime
import zipfile
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def build_exe():
    try:
        # Get the path to the root directory of the project
        root_dir = Path(__file__).parent.parent.absolute()
        logger.info(f"Root directory: {root_dir}")

        # Create pm_assistant directory
        pm_assistant_dir = root_dir / "assets" / "builds" / "pm_assistant"
        if pm_assistant_dir.exists():
            logger.info("Removing existing pm_assistant directory")
            shutil.rmtree(pm_assistant_dir)
        logger.info("Creating pm_assistant directory")
        pm_assistant_dir.mkdir(exist_ok=True)

        # Create spec file for PyInstaller
        logger.info("Creating spec file")
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{str(root_dir / "cli" / "start.py")}'],
    pathex=[r'{str(root_dir)}'],
    binaries=[],
    datas=[
        (r'{str(root_dir / "assets")}', 'assets'),
        (r'{str(root_dir / "src")}', 'src'),
        (r'{str(root_dir / "routers")}', 'routers'),
        (r'{str(root_dir / "services")}', 'services'),
        (r'{str(root_dir / "main.py")}', '.'),
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='task-allocation-system',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)"""

        # Write spec file
        spec_path = root_dir / "assets" / "builds" / "task-allocation-system.spec"
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)

        # Set environment variables for building llama-cpp-python
        logger.info("Setting up environment variables")
        os.environ["CMAKE_ARGS"] = (
            "-DGGML_AVX2=ON -DGGML_FMA=ON -DGGML_F16C=ON -DGGML_OPENMP=ON"
        )

        # Change to the backend directory before running PyInstaller
        logger.info("Changing to backend directory")
        os.chdir(root_dir)

        # Run PyInstaller
        logger.info("Starting PyInstaller build")
        PyInstaller.__main__.run(
            [
                str(spec_path),
                "--clean",
                "--noconfirm",
                "--distpath",
                str(pm_assistant_dir),
                "--workpath",
                str(pm_assistant_dir / "build"),
            ]
        )
        logger.info("PyInstaller build completed")

        # Delete spec file
        logger.info("Removing spec file")
        spec_path.unlink()

        # Create builds directory if it doesn't exist
        builds_dir = root_dir / "assets" / "builds"
        builds_dir.mkdir(parents=True, exist_ok=True)

        # Create zip archive
        logger.info("Creating zip archive")
        zip_path = builds_dir / f"pm_assistant.zip"

        total_files = sum([len(files) for _, _, files in os.walk(pm_assistant_dir)])
        processed_files = 0

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(pm_assistant_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, pm_assistant_dir)
                    logger.info(f"Adding to archive: {arcname}")
                    zipf.write(file_path, arcname)
                    processed_files += 1
                    if processed_files % 10 == 0:
                        logger.info(
                            f"Progress: {processed_files}/{total_files} files processed"
                        )

        logger.info("Zip archive created successfully")

        # Remove pm_assistant directory
        logger.info("Removing pm_assistant directory")
        shutil.rmtree(pm_assistant_dir)

        print("\nBuild completed!")
        print(f"Archive is located at: {zip_path}")
        print("\nUsage:")
        print("1. Start the system:")
        print("   ./task-allocation-system.exe")
        print("\n2. View logs:")
        print(
            "   ./task-allocation-system.exe --logs [--type TYPE] [--tail N] [--since HOURS]"
        )

    except Exception as e:
        logger.error(f"Build failed with error: {str(e)}")
        # Очистка в случае ошибки
        if "spec_path" in locals() and spec_path.exists():
            spec_path.unlink()
        if "pm_assistant_dir" in locals() and pm_assistant_dir.exists():
            shutil.rmtree(pm_assistant_dir)
        raise


if __name__ == "__main__":
    build_exe()
