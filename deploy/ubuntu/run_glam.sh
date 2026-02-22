#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  echo "[GLAM] Environnement virtuel introuvable: ${VENV_DIR}"
  echo "[GLAM] Exécutez d'abord: ${PROJECT_DIR}/deploy/ubuntu/install.sh"
  exit 1
fi

cd "${PROJECT_DIR}"

if [[ -f "${PROJECT_DIR}/deploy/ubuntu/glam.env" ]]; then
  set -a
  source "${PROJECT_DIR}/deploy/ubuntu/glam.env"
  set +a
fi

export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"
exec "${VENV_DIR}/bin/python" -m src.app
