#!/bin/sh

set -x

python - <<'EOF'
print("START")

import app.api.router

print("ROUTER IMPORTED")
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
