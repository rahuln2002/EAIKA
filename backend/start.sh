#!/bin/sh

set -x

python - <<'EOF'
print("analytics")
from app.api.routes.analytics import router

print("auth")
from app.api.routes.auth import router

print("chat")
from app.api.routes.chat import router

print("health")
from app.api.routes.health import router

print("search")
from app.api.routes.search import router

print("upload")
from app.api.routes.upload import router

print("websocket")
from app.api.routes.websocket import router

print("summarization")
from app.api.routes.summarization import router

print("DONE")
EOF

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
