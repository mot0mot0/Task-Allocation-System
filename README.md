# Task Allocation System Backend

Backend система для распределения задач между кандидатами с использованием LLM для анализа навыков.

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- PocketBase (включен в проект)
- LLM модель (Mistral-7B-Instruct-v0.3.Q4_K_S.gguf)

## Структура проекта

```
backend/
├── assets/
│   └── models/           # Директория для LLM моделей
├── cli/                  # CLI утилиты
│   ├── start.py         # Запуск сервисов
│   ├── build.py         # Сборка exe
│   └── logs.py          # Просмотр логов
├── logs/                # Логи приложения
├── pocketbase/          # PocketBase сервер
├── routers/            # API роутеры
├── services/           # Сервисы (LLM интерфейс)
├── src/                # Исходный код
│   ├── constants.py    # Константы
│   ├── pocketbase.py   # PocketBase клиент
│   └── schemas/        # Pydantic схемы
└── test_data/          # Тестовые данные
```

## Установка

1. Создайте виртуальное окружение:

```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:

- Windows:

```bash
venv\Scripts\activate
```

3. Установите зависимости:

```bash
install.ps1
```

4. Настройте переменные окружения:

- Windows:

```bash
set POCKETBASE_ADMIN_EMAIL=your_email
set POCKETBASE_ADMIN_PASSWORD=your_password
```

## Запуск

Используйте скрипт `start.py` для запуска всех сервисов:

```bash
python cli/start.py
```

Это запустит:

- PocketBase сервер на порту 8090
- FastAPI бэкенд на порту 8000

## API Endpoints

### Анализ задач и исполнителей

- POST `/analyze/tasks` - Анализ навыков, необходимых для задач
- POST `/analyze/executor` - Анализ навыков исполнителя

### Аутентификация

- POST `/auth/register` - Регистрация нового пользователя
- POST `/auth/token` - Получение токена доступа

### Сопоставление

- POST `/matching/match` - Сопоставление исполнителей с задачами

## Логирование

Логи сохраняются в директории `logs/`:

- `backend.log` - логи FastAPI сервера
- `llm.log` - логи LLM интерфейса
- `pocketbase.log` - логи PocketBase
- `startup.log` - логи запуска сервисов

Для просмотра логов используйте:

```bash
# Просмотр логов LLM (по умолчанию)
python cli/logs.py

# Просмотр логов бэкенда
python cli/logs.py --type backend

# Просмотр логов PocketBase
python cli/logs.py --type pocketbase

# Просмотр логов запуска
python cli/logs.py --type startup

# Просмотр последних N строк
python cli/logs.py --type backend --tail 100

# Просмотр логов за последние N часов
python cli/logs.py --type llm --since 24
```

## Сборка exe

Для создания исполняемого файла:

```bash
python cli/build.py
```

## Тестирование

Для тестирования анализа задач:

```bash
python test.py
```

## Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
