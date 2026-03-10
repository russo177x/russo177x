#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/carousel-studio"

if ! command -v docker >/dev/null 2>&1; then
  echo "[erro] Docker não encontrado no PATH." >&2
  exit 1
fi

cd "$APP_DIR"

echo "[info] Subindo stack com Docker Compose..."
docker compose up --build -d

echo "[info] Serviços iniciados."
echo "[info] Frontend: http://localhost:5173"
echo "[info] Backend:  http://localhost:8000"
echo "[info] Logs (tempo real): docker compose logs -f"
echo "[info] Parar tudo:         docker compose down"
