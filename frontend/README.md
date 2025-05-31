# Task Allocation System

Self-hosting система для распределения задач между кандидатами с использованием LLM для анализа навыков.

## Установка и запуск

### Установка из zip-архива (рекомендуется)

1. Скачайте последнюю версию `pm_assistant.zip` из директории `backend/assets/builds/`
2. Распакуйте архив в удобное место
3. Запустите `task-allocation-system.exe`

При первом запуске система автоматически:

- Скачает и установит PocketBase (версия 0.22.4)
- Скачает LLM модель Mistral-7B-Instruct-v0.3.Q4_K_S.gguf (~4GB)
- Создаст необходимые директории для логов
- Запустит все сервисы

### Установка из исходного кода

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-repo/task-allocation-system.git
cd task-allocation-system
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:

- Windows:

```bash
venv\Scripts\activate
```

4. Установите зависимости:

```bash
install.ps1
```

5. Настройте переменные окружения:

- Windows:

```bash
set POCKETBASE_ADMIN_EMAIL=your_email
set POCKETBASE_ADMIN_PASSWORD=your_password
```

## Использование системы

### Запуск через exe-файл

1. Запуск системы:

```bash
./task-allocation-system.exe
```

Система запустит:

- PocketBase сервер на порту 8090
- FastAPI бэкенд на порту 8000

2. Просмотр логов:

```bash
# Просмотр логов LLM (по умолчанию)
./task-allocation-system.exe --logs

# Просмотр логов бэкенда
./task-allocation-system.exe --logs --type backend

# Просмотр логов PocketBase
./task-allocation-system.exe --logs --type pocketbase

# Просмотр последних N строк
./task-allocation-system.exe --logs --type backend --tail 100

# Просмотр логов за последние N часов
./task-allocation-system.exe --logs --type llm --since 24
```

### Работа с базой данных

1. Откройте PocketBase Admin UI:

    - Перейдите по адресу: http://localhost:8090/\_/
    - При первом запуске создайте суперпользователя
    - Войдите используя email и пароль

2. Документация PocketBase:
    - [Официальная документация](https://pocketbase.io/docs/)
    - [API Reference](https://pocketbase.io/docs/api-authentication/)
    - [Collections](https://pocketbase.io/docs/collections/)

### API Endpoints

#### Аутентификация

```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

```http
POST /auth/token
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

#### Анализ задач и исполнителей

```http
POST /analyze/tasks
Content-Type: application/json
Authorization: Bearer your_token

{
    "tasks": [
        {
            "title": "Task title",
            "description": "Task description"
        }
    ]
}
```

```http
POST /analyze/executor
Content-Type: application/json
Authorization: Bearer your_token

{
    "skills": ["skill1", "skill2"],
    "experience": "Experience description"
}
```

#### Сопоставление

```http
POST /matching/match
Content-Type: application/json
Authorization: Bearer your_token

{
    "task_id": "task_id",
    "executor_id": "executor_id"
}
```

### Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- PocketBase (автоматически устанавливается)
- LLM модель (автоматически скачивается)
