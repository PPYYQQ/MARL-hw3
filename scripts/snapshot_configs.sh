#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HARL_DIR="${HARL_DIR:-${ROOT_DIR}/external/HARL}"
SNAPSHOT_DIR="${SNAPSHOT_DIR:-${ROOT_DIR}/configs/smac}"

require_file() {
  local path="$1"
  if [ ! -f "${path}" ]; then
    echo "Missing required config: ${path}" >&2
    exit 1
  fi
}

copy_config() {
  local source="$1"
  local target="$2"
  require_file "${source}"
  mkdir -p "$(dirname "${target}")"
  cp "${source}" "${target}"
  echo "wrote ${target}"
}

copy_config \
  "${HARL_DIR}/tuned_configs/smac/3s5z/happo/config.json" \
  "${SNAPSHOT_DIR}/3s5z/happo/config.json"

copy_config \
  "${HARL_DIR}/tuned_configs/smac/8m_vs_9m/happo/config.json" \
  "${SNAPSHOT_DIR}/8m_vs_9m/happo/config.json"

copy_config \
  "${ROOT_DIR}/results/processed/generated_mappo_3s5z.json" \
  "${SNAPSHOT_DIR}/3s5z/mappo/config.json"

copy_config \
  "${ROOT_DIR}/results/processed/generated_mappo_8m_vs_9m.json" \
  "${SNAPSHOT_DIR}/8m_vs_9m/mappo/config.json"
