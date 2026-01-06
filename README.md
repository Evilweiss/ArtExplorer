# Art Explorer MVP

Монорепо с FastAPI + Postgres и Next.js.

## Быстрый старт

### 1) Запуск Postgres

```bash
make postgres
```

### 2) Установка зависимостей

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
cd frontend
npm install
```

### 3) Миграции и seed

```bash
make migrate
make seed
```

### 4) Запуск сервисов (в разных терминалах)

```bash
make backend
```

```bash
make frontend
```

Откройте: `http://localhost:3000/van-gogh/starry-night`

## Переменные окружения

### Backend

- `DATABASE_URL` (по умолчанию `postgresql+asyncpg://postgres:postgres@localhost:5432/artexplorer`)

### Frontend

- `BACKEND_BASE_URL` (по умолчанию `http://localhost:8000`)

## Полезные команды

- Поднять Postgres: `make postgres`
- Миграции: `make migrate`
- Seed-данные: `make seed`
- Backend: `make backend`
- Frontend: `make frontend`
