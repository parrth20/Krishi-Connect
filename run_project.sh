#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt

cleanup() {
  if [ -n "${FASTAPI_PID:-}" ]; then
    kill "$FASTAPI_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

.venv/bin/python -m uvicorn chat_api.main:app --host 127.0.0.1 --port 8001 &
FASTAPI_PID=$!

echo "FastAPI chatbot: http://127.0.0.1:8001/docs"
echo "Django website:   http://127.0.0.1:8000"
echo "Farmer assistant: http://127.0.0.1:8000/assistant"

.venv/bin/python manage.py runserver 127.0.0.1:8000
