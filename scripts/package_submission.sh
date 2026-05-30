#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${DIST_DIR:-${ROOT_DIR}/dist}"
ASSIGNMENT_NAME="${ASSIGNMENT_NAME:-星际争霸对战}"

usage() {
  cat >&2 <<'USAGE'
Usage:
  STUDENT_ID=<id> STUDENT_NAME=<name> bash scripts/package_submission.sh

Optional:
  ASSIGNMENT_NAME=<name> DIST_DIR=<path> SKIP_VALIDATION=true
USAGE
}

require_env() {
  local name="$1"
  if [ -z "${!name:-}" ]; then
    echo "Missing required environment variable: ${name}" >&2
    usage
    exit 1
  fi
}

require_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing required command: ${command_name}" >&2
    exit 1
  fi
}

require_path() {
  local path="$1"
  if [ ! -e "${ROOT_DIR}/${path}" ]; then
    echo "Missing required path: ${path}" >&2
    exit 1
  fi
}

copy_item() {
  local path="$1"
  local source="${ROOT_DIR}/${path}"
  local target="${STAGE_DIR}/${path}"

  mkdir -p "$(dirname "${target}")"
  if [ -d "${source}" ]; then
    mkdir -p "${target}"
    cp -R "${source}/." "${target}/"
  else
    cp "${source}" "${target}"
  fi
}

require_env STUDENT_ID
require_env STUDENT_NAME
require_command zip
require_command python3

if [ "${SKIP_VALIDATION:-false}" != "true" ]; then
  (
    cd "${ROOT_DIR}"
    python3 scripts/validate_submission.py
  )
fi

REQUIRED_PATHS=(
  AGENTS.md
  README.md
  PROGRESS.md
  SUBMISSION.md
  TRAINING.md
  report/main.pdf
  report/main.tex
  report/report.html
  report/references.bib
  figures
  scripts
  configs
  logs
  results/processed
  results/raw/smoke
  results/raw/pilot
)

OPTIONAL_PATHS=(
  results/raw/full
)

for path in "${REQUIRED_PATHS[@]}"; do
  require_path "${path}"
done

STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "${STAGE_DIR}"' EXIT

for path in "${REQUIRED_PATHS[@]}"; do
  copy_item "${path}"
done

for path in "${OPTIONAL_PATHS[@]}"; do
  if [ -e "${ROOT_DIR}/${path}" ]; then
    copy_item "${path}"
  fi
done

mkdir -p "${DIST_DIR}"
DIST_DIR="$(cd "${DIST_DIR}" && pwd)"
ZIP_NAME="${STUDENT_ID}+${STUDENT_NAME}+${ASSIGNMENT_NAME}.zip"
ZIP_PATH="${DIST_DIR}/${ZIP_NAME}"

rm -f "${ZIP_PATH}"
(
  cd "${STAGE_DIR}"
  zip -qr "${ZIP_PATH}" . -x '*/__pycache__/*' '*/__pycache__/' '*.pyc' '*.pyo'
)

echo "Wrote ${ZIP_PATH}"
