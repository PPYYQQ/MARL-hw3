#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONDA_ENV="${CONDA_ENV:-harl_hw3}"

usage() {
  cat >&2 <<'USAGE'
Usage:
  STUDENT_ID=<id> STUDENT_NAME=<name> STUDENT_EMAIL=<email> bash scripts/prepare_submission.sh

Optional:
  ASSIGNMENT_NAME=<name> DIST_DIR=<path> CONDA_ENV=<env>
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

run_step() {
  echo "==> $*"
  "$@"
}

require_env STUDENT_ID
require_env STUDENT_NAME
require_env STUDENT_EMAIL
require_command python3
require_command bash
require_command conda

cd "${ROOT_DIR}"

run_step python3 scripts/apply_student_info.py
run_step bash scripts/snapshot_configs.sh
run_step python3 scripts/sync_harl_results.py --mode full
run_step python3 scripts/collect_progress.py
run_step python3 scripts/summarize_progress.py
run_step python3 scripts/check_full_training_status.py
run_step conda run -n "${CONDA_ENV}" python scripts/plot_win_rate.py
run_step bash scripts/build_report_pdf.sh
run_step python3 scripts/generate_artifact_manifest.py
run_step python3 scripts/validate_submission.py
run_step bash scripts/package_submission.sh
