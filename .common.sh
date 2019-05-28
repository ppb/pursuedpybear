set -euo pipefail

function run() {
    echo '$' "$@"
    "$@"
    echo
}

PY=${PY-python3}

if ! command -v $PY >/dev/null; then
    echo "Python interpreter '$PY' not found" >&2
    exit 1
fi
