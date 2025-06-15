import os
from pathlib import Path
import PyInstaller.__main__
import shutil
import zipfile
import logging
from logging.handlers import RotatingFileHandler
import datetime
import site
import glob

# Настройка логирования
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Создаем имя файла лога с текущей датой и временем
build_log_file = log_dir / f"build.log"

# Настраиваем форматтер для логов
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Настраиваем обработчик файла
file_handler = RotatingFileHandler(
    build_log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"  # 10MB
)
file_handler.setFormatter(log_formatter)

# Настраиваем обработчик консоли
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# Настраиваем логгер
logger = logging.getLogger("build")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def build_exe():
    spec_path = None
    pm_assistant_dir = None

    try:
        logger.info("Starting build process")
        # Получаем путь к корневой директории проекта
        root_dir = Path(__file__).parent.parent.absolute()
        logger.info(f"Root directory: {root_dir}")

        # Создаем директорию для сборки
        pm_assistant_dir = root_dir / "assets" / "builds" / "pm_assistant"
        if pm_assistant_dir.exists():
            logger.info("Removing existing pm_assistant directory")
            shutil.rmtree(pm_assistant_dir)
        logger.info("Creating pm_assistant directory")
        pm_assistant_dir.mkdir(exist_ok=True)

        # Создаем spec файл для PyInstaller
        logger.info("Creating spec file")

        # Получаем пути к DLL файлам
        site_packages = site.getsitepackages()[0]
        binaries = []

        # Добавляем DLL файлы llama-cpp-python
        llama_cpp_libs = glob.glob(
            os.path.join(site_packages, "llama_cpp", "lib", "*.dll")
        )
        for lib in llama_cpp_libs:
            binaries.append((lib, "llama_cpp/lib"))

        # Добавляем все необходимые DLL файлы
        for pkg in ["numpy", "llama_cpp", "fastapi", "uvicorn"]:
            pkg_path = os.path.join(site_packages, pkg)
            if os.path.exists(pkg_path):
                for root, dirs, files in os.walk(pkg_path):
                    for file in files:
                        if file.endswith(".dll"):
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(root, site_packages)
                            binaries.append((full_path, rel_path))

        spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{root_dir}/cli/start.py'],
    pathex=[r'{root_dir}'],
    binaries={binaries},
    datas=[
        (r'{root_dir}/assets', 'assets'),
        (r'{root_dir}/src', 'src'),
        (r'{root_dir}/routers', 'routers'),
        (r'{root_dir}/services', 'services'),
        (r'{root_dir}/main.py', '.'),
        (r'{root_dir}/requirements.txt', '.'),
        (r'{root_dir}/logs', 'logs'),
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
        'uvicorn.main',
        'uvicorn.config',
        'uvicorn.server',
        'uvicorn.workers',
        'threading',
        'asyncio',
        'fastapi',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'fastapi.middleware.trustedhost',
        'fastapi.middleware.gzip',
        'fastapi.middleware.httpsredirect',
        'fastapi.middleware.wsgi',
        'starlette',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.middleware.base',
        'starlette.middleware.exceptions',
        'starlette.middleware.sessions',
        'starlette.middleware.trustedhost',
        'starlette.middleware.gzip',
        'starlette.middleware.httpsredirect',
        'starlette.middleware.wsgi',
        'pydantic',
        'email_validator',
        'routers.auth',
        'routers.matching',
        'routers.analyzer',
        'routers.builds',
        'services.llm_interface',
        'src.pocketbase',
        'src.constants',
        'src.schemas',
        'logging',
        'logging.handlers',
        'pathlib',
        'socket',
        're',
        'requests',
        'tqdm',
        'argparse',
        'os',
        'sys',
        'subprocess',
        'signal',
        'time',
        'llama_cpp',
        'llama_cpp.llama_cpp',
        'llama_cpp._ctypes_extensions',
        'llama_cpp.llama_cpp_utils',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_avx2',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_avx512',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_f16c',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_fma',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_neon',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_sse3',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_sse4',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_sse41',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_sse42',
        'llama_cpp.llama_cpp_utils.llama_cpp_utils_ssse3',
        'numpy',
        'numpy.core._multiarray_umath',
        'numpy.core._multiarray_tests',
        'numpy.linalg._umath_linalg',
        'numpy.linalg.lapack_lite',
        'numpy.random.mtrand',
        'numpy.random._bounded_integers',
        'numpy.random._common',
        'numpy.random._generator',
        'numpy.random._mt19937',
        'numpy.random._pcg64',
        'numpy.random._philox',
        'numpy.random._sfc64',
        'numpy.random.bit_generator',
        'numpy.fft._pocketfft_umath',
        'numpy.fft._pocketfft_internal',
        'numpy.fft.helper',
        'numpy.fft',
        'numpy.core._dtype_ctypes',
        'numpy.core._methods',
        'numpy.core._dtype',
        'numpy.core._internal',
        'numpy.core._umath_tests',
        'numpy.core._rational_tests',
        'numpy.core._struct_ufunc_tests',
        'numpy.core._operand_flag_tests',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

# Исключаем модель из сборки
a.datas = [x for x in a.datas if not x[0].endswith('.gguf')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pm_assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pm_assistant',
)""".format(
            root_dir=str(root_dir), binaries=binaries
        )

        # Записываем spec файл
        spec_path = root_dir / "assets" / "builds" / "pm_assistant.spec"
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        logger.info(f"Spec file created at: {spec_path}")

        # Устанавливаем переменные окружения для сборки llama-cpp-python
        logger.info("Setting up environment variables")
        os.environ["CMAKE_ARGS"] = (
            "-DGGML_AVX2=ON -DGGML_FMA=ON -DGGML_F16C=ON -DGGML_OPENMP=ON"
        )

        # Переходим в директорию backend перед запуском PyInstaller
        logger.info("Changing to backend directory")
        os.chdir(root_dir)

        # Запускаем PyInstaller
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
                "--log-level=DEBUG",  # Добавляем подробное логирование
            ]
        )
        logger.info("PyInstaller build completed")

        # Удаляем spec файл
        logger.info("Removing spec file")
        spec_path.unlink()

        # Создаем директорию builds если она не существует
        builds_dir = root_dir / "assets" / "builds"
        builds_dir.mkdir(parents=True, exist_ok=True)

        # Перемещаем содержимое pm_assistant в корень
        pm_assistant_build_dir = pm_assistant_dir / "pm_assistant"
        if pm_assistant_build_dir.exists():
            logger.info("Moving files to root directory")
            for item in pm_assistant_build_dir.iterdir():
                target = pm_assistant_dir / item.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                shutil.move(str(item), str(target))
            shutil.rmtree(pm_assistant_build_dir)

        # Создаем директорию llama_cpp/lib в _internal
        logger.info("Creating llama_cpp/lib directory")
        llama_cpp_lib_dir = pm_assistant_dir / "_internal" / "llama_cpp" / "lib"
        llama_cpp_lib_dir.mkdir(parents=True, exist_ok=True)

        # Копируем DLL файлы в llama_cpp/lib
        logger.info("Copying DLL files to llama_cpp/lib")
        site_packages = site.getsitepackages()[0]
        llama_cpp_libs = glob.glob(
            os.path.join(site_packages, "llama_cpp", "lib", "*.dll")
        )
        for lib in llama_cpp_libs:
            shutil.copy2(lib, llama_cpp_lib_dir)

        # Создаем zip архив
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
                        logger.info(f"Progress: {processed_files}/{total_files} files processed")
        
        logger.info("Zip archive created successfully")
        
        # Удаляем директорию pm_assistant
        logger.info("Removing pm_assistant directory")
        shutil.rmtree(pm_assistant_dir)

        logger.info("\nBuild completed!")
        logger.info(f"Application is located at: {pm_assistant_dir}")
        # logger.info(f"Archive is located at: {zip_path}")
        logger.info("\nUsage:")
        logger.info("1. Start the system:")
        logger.info("   ./pm_assistant.exe")
        logger.info("\n2. View logs:")
        logger.info(
            "   ./pm_assistant.exe --logs [--type TYPE] [--tail N] [--since HOURS]"
        )

    except Exception as e:
        logger.error(f"Build failed with error: {str(e)}", exc_info=True)
        # Очистка в случае ошибки
        if spec_path and spec_path.exists():
            spec_path.unlink()
        if pm_assistant_dir and pm_assistant_dir.exists():
            shutil.rmtree(pm_assistant_dir)
        raise


if __name__ == "__main__":
    build_exe()
