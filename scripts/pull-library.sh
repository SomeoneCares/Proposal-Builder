#!/usr/bin/env bash
# Copy module versions and figures saved in the portal's Module Library into this repo,
# so they can be reviewed with `git diff` and committed.
#
# Usage: scripts/pull-library.sh
set -euo pipefail

HOST=${DEPLOY_HOST:-hermes@192.168.100.178}
PY='proposal-builder/venv/bin/python'

cd "$(dirname "$0")/.."

ssh "$HOST" "~/$PY - <<'PY'
import json, pathlib
home = pathlib.Path.home()
index = json.loads((home / '.hermes/skills/proposal-template/module_index.json').read_text())
lib = home / 'proposal-builder/library/modules'
for group in index['modules'].values():
    for mod in group['modules']:
        if (lib / mod['token'] / 'current.md').is_file():
            print(mod['token'], mod['file'])
PY" | while read -r token file; do
  scp -q "$HOST:proposal-builder/library/modules/$token/current.md" "$file"
  echo "pulled $token -> $file"
done

mkdir -p assets/figures
if ssh "$HOST" 'ls ~/proposal-builder/library/figures/* >/dev/null 2>&1'; then
  scp -q "$HOST:proposal-builder/library/figures/*" assets/figures/
  echo "pulled figures -> assets/figures/"
fi

git status --short modules assets/figures
