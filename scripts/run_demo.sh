#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT_DIR/.venv"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "Creating virtual environment .venv..."
  python3 -m venv "$VENV"
fi

"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r "$ROOT_DIR/requirements.txt"

"$PY" -m modern_python_demo "$@"
