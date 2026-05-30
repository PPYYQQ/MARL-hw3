#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${ENV_NAME:-harl_hw3}"
PYTHON_VERSION="${PYTHON_VERSION:-3.10}"
HARL_DIR="${HARL_DIR:-external/HARL}"
TORCH_INDEX_URL="${TORCH_INDEX_URL:-}"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda is required but was not found." >&2
  exit 1
fi

if [ ! -d "${HARL_DIR}/.git" ]; then
  mkdir -p "$(dirname "${HARL_DIR}")"
  git clone https://github.com/PKU-MARL/HARL.git "${HARL_DIR}"
fi

eval "$(conda shell.bash hook)"

if ! conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
  conda create -y -n "${ENV_NAME}" "python=${PYTHON_VERSION}"
fi

conda activate "${ENV_NAME}"
python -m pip install --upgrade pip "setuptools<82" wheel

if [ -n "${TORCH_INDEX_URL}" ]; then
  python -m pip install torch --index-url "${TORCH_INDEX_URL}"
fi

python -m pip install -e "${HARL_DIR}"
python -m pip install "numpy<1.24" matplotlib pandas
python -m pip uninstall -y smac >/dev/null 2>&1 || true
python -m pip install "git+https://github.com/oxwhirl/smac.git"
conda install -y -c conda-forge gym=0.21.0
python -m pip install pyglet==1.5.0 importlib-metadata==4.13.0
python -m pip install --force-reinstall --no-cache-dir "numpy<1.24"

python - <<'PY'
import importlib.util
import sys

checks = ["torch", "harl", "matplotlib"]
for name in checks:
    spec = importlib.util.find_spec(name)
    status = "ok" if spec else "missing"
    print(f"{name}: {status}")

try:
    from smac.env import StarCraft2Env
    print("smac.env.StarCraft2Env: ok")
except Exception as exc:
    print("SMAC import failed:", exc, file=sys.stderr)

try:
    import torch
    print("torch:", torch.__version__, "cuda:", torch.cuda.is_available())
except Exception as exc:
    print("torch import failed:", exc, file=sys.stderr)
PY

if [ -z "${SC2PATH:-}" ]; then
  echo "SC2PATH is not set. Set it before running SMAC training."
else
  echo "SC2PATH=${SC2PATH}"
fi
