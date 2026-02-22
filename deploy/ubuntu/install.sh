#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"

SUDO=""
if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
fi

echo "[GLAM] Installation Ubuntu - dossier projet: ${PROJECT_DIR}"

${SUDO} apt-get update
${SUDO} apt-get install -y \
  python3 \
  python3-venv \
  python3-pip \
  python3-dev \
  build-essential \
  libgl1 \
  libglib2.0-0 \
  libegl1 \
  libdbus-1-3 \
  libxkbcommon-x11-0 \
  libxcb-cursor0 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-randr0 \
  libxcb-render-util0 \
  libxcb-shape0 \
  libxcb-xfixes0

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/pip" install --upgrade pip wheel setuptools
"${VENV_DIR}/bin/pip" install -r "${PROJECT_DIR}/requirements.txt"

mkdir -p "${PROJECT_DIR}/logs" "${PROJECT_DIR}/data"

if id -nG "${USER}" | grep -qw dialout; then
  echo "[GLAM] Utilisateur ${USER} déjà dans le groupe dialout"
else
  echo "[GLAM] Ajout de ${USER} au groupe dialout (Arduino/USB série)"
  ${SUDO} usermod -aG dialout "${USER}"
  echo "[GLAM] Reconnectez votre session pour prendre en compte le groupe dialout"
fi

echo "[GLAM] Installation terminée"
echo "[GLAM] Lancez l'application avec: ${PROJECT_DIR}/deploy/ubuntu/run_glam.sh"
