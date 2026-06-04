# Todo App Backend

Экспериментальный пет-проект по изучению слоистой архитектуры FastAPI-бэкенда.
Реализует CRUD для задач (tasks) и категорий (categories) — без связи между ними, чтобы не усложнять учебный пример.

## Стек

- **Python 3.12** / **FastAPI** / **Uvicorn**
- **SQLAlchemy 2** (ORM, синхронный движок)
- **PostgreSQL 16** (через `psycopg`)
- **Pydantic v2** + **pydantic-settings**
- **Docker Compose** (бэкенд + БД + фронтенд)

## Архитектура

```
app/
├── api/
│   ├── dependencies.py      # Dependency Injection (сервисы)
│   └── routers/
│       ├── task.py           # Эндпоинты задач
│       └── category.py       # Эндпоинты категорий
├── core/
│   └── config.py             # Настройки (pydantic-settings, .env)
├── db/
│   └── session.py            # Engine, SessionLocal, get_db
├── models/
│   ├── base.py               # Базовая ORM-модель (UUID PK)
│   ├── task.py               # TaskORM
│   └── category.py           # CategoryORM
├── repositories/
│   ├── task.py               # Доступ к БД — задачи
│   └── category.py           # Доступ к БД — категории
├── schemas/
│   ├── task.py               # Pydantic-схемы задач
│   └── category.py           # Pydantic-схемы категорий
├── services/
│   ├── task.py               # Бизнес-логика задач
│   └── category.py           # Бизнес-логика категорий
└── main.py                   # Точка входа, lifespan, CORS
```

Слои: **Router → Service → Repository → ORM / DB**.

## Запуск (Docker Compose)

```bash
docker compose up --build
```

Будут подняты три сервиса:

| Сервис     | URL                    |
|------------|------------------------|
| Backend    | http://localhost:8000   |
| Frontend   | http://localhost:3000   |
| PostgreSQL | localhost:15432         |

## Запуск без Docker

1. Поднять PostgreSQL и создать базу.
2. Создать `.env` в корне проекта:
   ```
   DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:15432/postgres
   ```
3. Установить зависимости и запустить:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

## API

Базовый URL: `http://localhost:8000`

### Задачи (`/tasks`)

| Метод    | Путь            | Описание         | Статус  |
|----------|-----------------|------------------|---------|
| `GET`    | `/tasks/`       | Список задач     | 200     |
| `POST`   | `/tasks/`       | Создать задачу   | 201     |
| `PATCH`  | `/tasks/{id}`   | Обновить задачу  | 200     |
| `DELETE` | `/tasks/{id}`   | Удалить задачу   | 204     |

### Категории (`/categories`)

| Метод    | Путь                | Описание            | Статус  |
|----------|---------------------|---------------------|---------|
| `GET`    | `/categories`       | Список категорий    | 200     |
| `POST`   | `/categories`       | Создать категорию   | 201     |
| `PATCH`  | `/categories/{id}`  | Обновить категорию  | 200     |
| `DELETE` | `/categories/{id}`  | Удалить категорию   | 204     |

Интерактивная документация: http://localhost:8000/docs

## Фронтенд

В папке `todo-app-frontend-master/` находится готовый React-фронтенд (учебный CRUD-шаблон).
При запуске через Docker Compose поднимается автоматически на http://localhost:3000.

Для ручного запуска:

```bash
cd todo-app-frontend-master
npm install
npm run dev
```
