#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/carousel-studio"
BACKEND_DIR="$APP_DIR/backend"
FRONTEND_DIR="$APP_DIR/frontend"
VENV_DIR="$ROOT_DIR/.venv-carousel-studio"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[erro] Comando obrigatório não encontrado: $1" >&2
    exit 1
  fi
}

require_cmd python3
require_cmd npm

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[warn] ffmpeg não encontrado. Export MP4 ficará indisponível, PNG+ZIP continuarão funcionando."
fi

echo "[info] Criando/atualizando ambiente virtual isolado em: $VENV_DIR"
python3 -m venv "$VENV_DIR"
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
pip install -r "$BACKEND_DIR/requirements.txt"

echo "[info] Instalando dependências do frontend"
cd "$FRONTEND_DIR"
npm install

cd "$ROOT_DIR"

echo "[info] Iniciando backend (uvicorn) em segundo plano..."
(
  cd "$BACKEND_DIR"
  "$VENV_DIR/bin/uvicorn" main:app --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!

cleanup() {
  if ps -p "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

sleep 1

echo "[info] Iniciando frontend (vite) em primeiro plano..."
echo "[info] Frontend: http://localhost:5173"
echo "[info] Backend:  http://localhost:8000"
cd "$FRONTEND_DIR"
npm run dev -- --host 0.0.0.0 --port 5173
