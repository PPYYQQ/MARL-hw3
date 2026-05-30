#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-}"
GITHUB_USERNAME="${GITHUB_USERNAME:-x-access-token}"

usage() {
  cat >&2 <<'USAGE'
Usage:
  bash scripts/push_to_github.sh

Optional:
  GITHUB_TOKEN=<token> GITHUB_USERNAME=<username> REMOTE=origin BRANCH=main PUSH_DRY_RUN=true

Notes:
  - If GITHUB_TOKEN is set, this script uses a temporary GIT_ASKPASS helper.
  - The token is not written to git remote URLs or repository files.
USAGE
}

require_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing required command: ${command_name}" >&2
    exit 1
  fi
}

require_command git

cd "${ROOT_DIR}"

if [ ! -d .git ]; then
  echo "Not a git repository: ${ROOT_DIR}" >&2
  exit 1
fi

if [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ -z "${BRANCH}" ]; then
  BRANCH="$(git branch --show-current)"
fi

if [ -z "${BRANCH}" ]; then
  echo "Cannot determine current branch; set BRANCH explicitly." >&2
  exit 1
fi

remote_url="$(git remote get-url "${REMOTE}")"

echo "remote=${REMOTE}"
echo "url=${remote_url}"
echo "branch=${BRANCH}"

if [ "${PUSH_DRY_RUN:-false}" = "true" ]; then
  echo "dry_run=true"
  git status --short --branch
  git log --oneline -5
  exit 0
fi

if [ -n "${GITHUB_TOKEN:-}" ]; then
  askpass_dir="$(mktemp -d)"
  trap 'rm -rf "${askpass_dir}"' EXIT
  askpass="${askpass_dir}/askpass.sh"
  cat >"${askpass}" <<'SH'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf '%s\n' "${GITHUB_USERNAME:-x-access-token}" ;;
  *Password*) printf '%s\n' "${GITHUB_TOKEN:?}" ;;
  *) printf '\n' ;;
esac
SH
  chmod 700 "${askpass}"
  GIT_ASKPASS="${askpass}" GIT_TERMINAL_PROMPT=0 git push -u "${REMOTE}" "${BRANCH}"
else
  GIT_TERMINAL_PROMPT=0 git push -u "${REMOTE}" "${BRANCH}"
fi
