#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HTML_PATH="${HTML_PATH:-${ROOT_DIR}/report/report.html}"
PDF_PATH="${PDF_PATH:-${ROOT_DIR}/report/main.pdf}"
CHROME_BIN="${CHROME_BIN:-}"

if [ -z "${CHROME_BIN}" ]; then
  for candidate in /opt/google/chrome/google-chrome google-chrome chromium chromium-browser; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      CHROME_BIN="$(command -v "${candidate}")"
      break
    fi
  done
fi

if [ -z "${CHROME_BIN}" ]; then
  echo "Chrome/Chromium is required to build ${PDF_PATH} from ${HTML_PATH}." >&2
  exit 1
fi

HTML_URI="$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve().as_uri())' "${HTML_PATH}")"
PROFILE_DIR="$(mktemp -d)"
trap 'rm -rf "${PROFILE_DIR}"' EXIT

timeout 60s "${CHROME_BIN}" \
  --headless=new \
  --disable-gpu \
  --disable-dev-shm-usage \
  --no-sandbox \
  --no-first-run \
  --user-data-dir="${PROFILE_DIR}" \
  --print-to-pdf="${PDF_PATH}" \
  "${HTML_URI}"

echo "wrote ${PDF_PATH}"
