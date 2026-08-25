#!/usr/bin/env bash
# Set up the EasySpider execution stage (https://github.com/NaiboWang/EasySpider).
#
# EasySpider has two halves:
#   1. the Electron GUI, where you design a scraping task by clicking a page
#   2. the ExecuteStage CLI, which replays a saved task headlessly
#
# The GUI is a desktop download and is NOT installed here. This script sets up
# the CLI half, which is what an agent can actually drive.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${EASYSPIDER_HOME:-${ROOT}/vendor/EasySpider}"

echo "==> Checking prerequisites"
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found (EasySpider needs Python 3.7+)." >&2
  exit 1
fi
python3 - <<'PY' || exit 1
import sys
if sys.version_info < (3, 7):
    sys.exit(f"ERROR: Python 3.7+ required, found {sys.version.split()[0]}")
PY
echo "    python3: $(python3 --version)"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git not found." >&2
  exit 1
fi

echo "==> Fetching EasySpider source into ${DEST}"
if [ -d "${DEST}/.git" ]; then
  git -C "$DEST" pull --ff-only
else
  mkdir -p "$(dirname "$DEST")"
  # Only the execution stage is needed; a shallow clone keeps this quick.
  git clone --depth 1 https://github.com/NaiboWang/EasySpider.git "$DEST"
fi

echo "==> Installing ExecuteStage dependencies"
VENV="${DEST}/.venv"
[ -d "$VENV" ] || python3 -m venv "$VENV"
"${VENV}/bin/pip" install --upgrade pip >/dev/null
"${VENV}/bin/pip" install -r "${DEST}/ExecuteStage/requirements.txt"

cat <<NOTE

==> Done.

  Source:      ${DEST}
  Interpreter: ${VENV}/bin/python

Run a saved task (task id 1, headless, reading its config from disk):

  cd ${DEST}/ExecuteStage
  ${VENV}/bin/python easyspider_executestage.py \\
      --ids [1] --read_type local --headless 1 \\
      --config_folder /path/to/your/task/configs

Task JSON files come from the EasySpider desktop GUI, which you design tasks
in and download separately:
  https://github.com/NaiboWang/EasySpider/releases

The CLI also needs a Chrome binary plus a matching chromedriver on PATH (the
GUI bundles its own). Full argument reference:
  https://github.com/NaiboWang/EasySpider/wiki/Argument-Instruction

Only scrape sites whose terms of service and robots.txt permit it.
NOTE
