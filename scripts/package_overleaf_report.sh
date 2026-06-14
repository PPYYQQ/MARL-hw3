#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${DIST_DIR:-${ROOT_DIR}/dist}"
ZIP_NAME="${ZIP_NAME:-marl_hw3_overleaf.zip}"

require_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing required command: ${command_name}" >&2
    exit 1
  fi
}

copy_required() {
  local source="$1"
  local target="$2"
  if [ ! -f "${ROOT_DIR}/${source}" ]; then
    echo "Missing required file: ${source}" >&2
    exit 1
  fi
  mkdir -p "$(dirname "${target}")"
  cp "${ROOT_DIR}/${source}" "${target}"
}

require_command zip

STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "${STAGE_DIR}"' EXIT

copy_required report/main.tex "${STAGE_DIR}/main.tex"
copy_required report/references.bib "${STAGE_DIR}/references.bib"
copy_required report/icml2022.sty "${STAGE_DIR}/icml2022.sty"
copy_required report/icml2022.bst "${STAGE_DIR}/icml2022.bst"
copy_required report/algorithm.sty "${STAGE_DIR}/algorithm.sty"
copy_required report/algorithmic.sty "${STAGE_DIR}/algorithmic.sty"
copy_required report/fancyhdr.sty "${STAGE_DIR}/fancyhdr.sty"
copy_required figures/teaser_smac_8m_vs_9m.png "${STAGE_DIR}/figures/teaser_smac_8m_vs_9m.png"
copy_required figures/win_rate_3s5z.png "${STAGE_DIR}/figures/win_rate_3s5z.png"
copy_required figures/win_rate_8m_vs_9m.png "${STAGE_DIR}/figures/win_rate_8m_vs_9m.png"

cat >"${STAGE_DIR}/README.md" <<'README'
# MARL HW3 Overleaf Project

Upload this zip directly to Overleaf. The entry point is `main.tex`.

Suggested compiler: pdfLaTeX.

The report keeps placeholder identity fields:
- `Student Name`
- `Student ID: TODO`
- `email@example.com`

Replace them in `main.tex` before final submission.
README

mkdir -p "${DIST_DIR}"
DIST_DIR="$(cd "${DIST_DIR}" && pwd)"
ZIP_PATH="${DIST_DIR}/${ZIP_NAME}"

rm -f "${ZIP_PATH}"
(
  cd "${STAGE_DIR}"
  zip -qr "${ZIP_PATH}" .
)

echo "Wrote ${ZIP_PATH}"
