#!/bin/sh

python - <<'EOF'
print("1")
from app.api.middleware import setup_auth_middleware
print("2")
from app.core.config import settings
print("3")
from app.exceptions import register_exception_handlers
print("4")
from app.monitoring.prometheus import router
print("5")
from app.monitoring.healthcheck import healthcheck
print("6")
from app.api.router import api_router
print("7")

echo "Waiting for PostgreSQL..."

sleep 15

echo "Running Alembic migrations..."

alembic upgrade head

echo "Starting FastAPI..."
echo "PORT=$PORT"

uvicorn app.main:app \
	--host 0.0.0.0 \
	--port ${PORT} \
	--log-level debug
