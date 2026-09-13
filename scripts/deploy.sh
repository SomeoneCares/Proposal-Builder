#!/usr/bin/env bash
# Deploy this repo to the Hermes lab host.
#
# 1. Copies the working tree (tracked + untracked, minus .gitignore) to ~/proposal-template-staging
# 2. Runs the test suite there with the Hermes venv python
# 3. Swaps it into ~/.hermes/skills/proposal-template (previous copy kept in ~/proposal-template-previous)
# 4. Copies hermes-profile/SKILL.md + references into the bid-orchestrator profile
# 5. Restarts the proposal-builder user unit and checks it answers
#
# Usage: scripts/deploy.sh [--test-only]
set -euo pipefail

HOST=${DEPLOY_HOST:-hermes@192.168.100.178}
LIVE='.hermes/skills/proposal-template'
PROFILE_SKILL='.hermes/profiles/bid-orchestrator/skills/proposal-template'
STAGE='proposal-template-staging'
PREVIOUS='proposal-template-previous'
PY='.hermes/hermes-agent/venv/bin/python'

cd "$(dirname "$0")/.."

echo "== copying working tree to $HOST:~/$STAGE"
ssh "$HOST" "rm -rf ~/$STAGE && mkdir -p ~/$STAGE"
git ls-files -z --cached --others --exclude-standard \
  | tar --null -T - -cf - \
  | ssh "$HOST" "tar -xf - -C ~/$STAGE"

echo "== running tests on the host"
ssh "$HOST" "cd ~/$STAGE && ~/$PY -B -m unittest discover -s tests"

if [[ "${1:-}" == "--test-only" ]]; then
  echo "== tests passed; --test-only, not deploying"
  exit 0
fi

echo "== swapping into ~/$LIVE"
ssh "$HOST" "set -e
  rm -rf ~/$PREVIOUS
  cp -a ~/$LIVE ~/$PREVIOUS
  rm -rf ~/$STAGE/hermes-profile.tmp && mv ~/$STAGE/hermes-profile ~/$STAGE/hermes-profile.tmp
  mkdir -p ~/$PROFILE_SKILL/references
  cp ~/$STAGE/hermes-profile.tmp/SKILL.md ~/$PROFILE_SKILL/SKILL.md
  cp ~/$STAGE/hermes-profile.tmp/references/*.md ~/$PROFILE_SKILL/references/
  rm -rf ~/$STAGE/hermes-profile.tmp
  rm -rf ~/$LIVE.new && mv ~/$STAGE ~/$LIVE.new
  rm -rf ~/$LIVE && mv ~/$LIVE.new ~/$LIVE"

echo "== restarting proposal-builder"
ssh "$HOST" "systemctl --user restart proposal-builder && sleep 4 \
  && systemctl --user is-active proposal-builder \
  && curl -fsS -o /dev/null -w 'builder HTTP %{http_code}\n' http://127.0.0.1:8501/_stcore/health"

echo "== deployed $(git rev-parse --short HEAD)$(git diff --quiet && echo '' || echo ' + uncommitted changes')"
