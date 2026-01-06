.PHONY: postgres migrate seed backend frontend dev

postgres:
	docker compose up -d postgres

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m app.seed

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

dev: postgres migrate seed
	@echo "Run 'make backend' and 'make frontend' in separate terminals"
