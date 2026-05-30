#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-smoke}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HARL_DIR="${HARL_DIR:-${ROOT_DIR}/external/HARL}"
EXP_PREFIX="${EXP_PREFIX:-hw3}"
SEEDS="${SEEDS:-1}"
MAPS="${MAPS:-3s5z 8m_vs_9m}"
ALGOS="${ALGOS:-mappo happo}"
CUDA="${CUDA:-true}"
DRY_RUN="false"
PRINT_ONLY="${PRINT_ONLY:-false}"

if [ ! -d "${HARL_DIR}/examples" ]; then
  echo "HARL_DIR is invalid: ${HARL_DIR}" >&2
  exit 1
fi

case "${MODE}" in
  dry-run)
    DRY_RUN="true"
    EXTRA_ARGS=(--num_env_steps 1000 --n_rollout_threads 1 --n_eval_rollout_threads 1 --eval_episodes 1 --log_interval 1 --eval_interval 1)
    ;;
  smoke)
    EXTRA_ARGS=(--num_env_steps 1000 --n_rollout_threads 1 --n_eval_rollout_threads 1 --eval_episodes 1 --log_interval 1 --eval_interval 1)
    ;;
  pilot)
    EXTRA_ARGS=(
      --num_env_steps "${PILOT_NUM_ENV_STEPS:-10000}"
      --n_rollout_threads "${PILOT_N_ROLLOUT_THREADS:-1}"
      --n_eval_rollout_threads "${PILOT_N_EVAL_ROLLOUT_THREADS:-1}"
      --eval_episodes "${PILOT_EVAL_EPISODES:-1}"
      --log_interval "${PILOT_LOG_INTERVAL:-5}"
      --eval_interval "${PILOT_EVAL_INTERVAL:-5}"
    )
    ;;
  full)
    EXTRA_ARGS=()
    ;;
  *)
    echo "Usage: $0 [dry-run|smoke|pilot|full]" >&2
    exit 1
    ;;
esac

if [ "${CUDA}" = "false" ]; then
  EXTRA_ARGS+=(--cuda False)
fi

if [ "${PRINT_ONLY}" = "true" ]; then
  DRY_RUN="true"
fi

generate_mappo_config() {
  local map_name="$1"
  local src="${HARL_DIR}/tuned_configs/smac/${map_name}/happo/config.json"
  local out="${ROOT_DIR}/results/processed/generated_mappo_${map_name}.json"

  if [ ! -f "${src}" ]; then
    echo "Cannot generate MAPPO config; missing HAPPO source: ${src}" >&2
    exit 1
  fi

  python - "${src}" "${out}" <<'PY'
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
config = json.loads(src.read_text(encoding="utf-8"))
config["main_args"]["algo"] = "mappo"
config["main_args"]["env"] = "smac"
config["algo_args"]["algo"]["share_param"] = True
config["algo_args"]["algo"]["fixed_order"] = True
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(config, indent=4, sort_keys=True), encoding="utf-8")
print(out)
PY
}

config_for() {
  local algo="$1"
  local map_name="$2"
  local tuned="${HARL_DIR}/tuned_configs/smac/${map_name}/${algo}/config.json"

  if [ -f "${tuned}" ]; then
    realpath "${tuned}"
  elif [ "${algo}" = "mappo" ]; then
    generate_mappo_config "${map_name}"
  else
    echo "No config for ${algo}/${map_name}" >&2
    exit 1
  fi
}

for map_name in ${MAPS}; do
  for algo in ${ALGOS}; do
    config_path="$(config_for "${algo}" "${map_name}")"
    for seed in ${SEEDS}; do
      exp_name="${EXP_PREFIX}_${MODE}_${algo}_${map_name}"
      echo "Running ${algo} on ${map_name}, seed ${seed}, mode ${MODE}"
      command=(
        python train.py
        --load_config "${config_path}"
        --exp_name "${exp_name}"
        --seed "${seed}"
        "${EXTRA_ARGS[@]}"
      )
      printf 'cd %q &&' "${HARL_DIR}/examples"
      printf ' %q' "${command[@]}"
      printf '\n'
      if [ "${DRY_RUN}" = "true" ]; then
        continue
      fi
      (
        cd "${HARL_DIR}/examples"
        "${command[@]}"
      )
    done
  done
done
