install:
	pip install -r backend/requirements.txt

run-backend:
	cd backend && uvicorn app.main:app --reload

run-frontend:
	cd frontend && npm run dev

lint:
	ruff check .

format:
	black .

test:
	pytest

up:
	docker compose -f infrastructure/docker/docker-compose.yml up --build

down:
	docker compose -f infrastructure/docker/docker-compose.yml down
