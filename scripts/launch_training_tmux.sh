#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-${MODE:-full}}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONDA_ENV="${CONDA_ENV:-harl_hw3}"
SESSION="${SESSION:-hw3_${MODE}_$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/logs/training_sessions}"
LOG_FILE="${LOG_FILE:-${LOG_DIR}/${SESSION}.log}"

usage() {
  cat >&2 <<'USAGE'
Usage:
  bash scripts/launch_training_tmux.sh [pilot|full]

Optional environment:
  SESSION=<tmux-session> CONDA_ENV=<env> MAPS=<maps> ALGOS=<algos> SEEDS=<seeds>
  EXP_PREFIX=<prefix> CUDA=<true|false> LOG_FILE=<path> LAUNCH_DRY_RUN=true
USAGE
}

require_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing required command: ${command_name}" >&2
    exit 1
  fi
}

case "${MODE}" in
  pilot|full)
    ;;
  *)
    usage
    exit 1
    ;;
esac

require_command tmux
require_command conda

mkdir -p "${LOG_DIR}"

if tmux has-session -t "${SESSION}" >/dev/null 2>&1; then
  echo "tmux session already exists: ${SESSION}" >&2
  exit 1
fi

command=(
  env
  "MAPS=${MAPS:-3s5z 8m_vs_9m}"
  "ALGOS=${ALGOS:-mappo happo}"
  "SEEDS=${SEEDS:-1}"
  "EXP_PREFIX=${EXP_PREFIX:-hw3_${MODE}}"
  "CUDA=${CUDA:-true}"
  conda run -n "${CONDA_ENV}" bash scripts/run_smac_experiments.sh "${MODE}"
)

printf -v command_string " %q" "${command[@]}"
command_string="${command_string:1}"
run_command="set -euo pipefail; cd $(printf "%q" "${ROOT_DIR}"); ${command_string} 2>&1 | tee -a $(printf "%q" "${LOG_FILE}")"

echo "session=${SESSION}"
echo "log=${LOG_FILE}"
echo "command=${command_string}"

if [ "${LAUNCH_DRY_RUN:-false}" = "true" ]; then
  echo "dry_run=true"
  exit 0
fi

tmux new-session -d -s "${SESSION}" bash -lc "${run_command}"
echo "started tmux session: ${SESSION}"
echo "attach: tmux attach -t ${SESSION}"
