#!/bin/sh

set -x

python - <<'EOF'
print("before service")

from app.services.chat.chat_service import ChatService

print("after service")
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
