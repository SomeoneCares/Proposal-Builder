#!/usr/bin/env bash
# Load the Proposal Builder image and start it. Safe to run again (upgrades in place).
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker Engine with the Compose plugin: https://docs.docker.com/engine/install/" >&2
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  password=$(head -c 18 /dev/urandom | base64 | tr -d '/+=' | cut -c1-16)
  sed -i "s/^PROPOSAL_EDITOR_PASSWORD=.*/PROPOSAL_EDITOR_PASSWORD=$password/" .env
  chmod 600 .env
  echo "Created .env. Module Library editor password: $password (stored in .env)"
else
  # Keep the operator's settings but move the image tag to this bundle's version.
  tag=$(grep '^PROPOSAL_BUILDER_TAG=' .env.example | cut -d= -f2)
  if grep -q '^PROPOSAL_BUILDER_TAG=' .env; then
    sed -i "s/^PROPOSAL_BUILDER_TAG=.*/PROPOSAL_BUILDER_TAG=$tag/" .env
  else
    printf 'PROPOSAL_BUILDER_TAG=%s\n' "$tag" >> .env
  fi
fi

echo "Loading the image..."
docker load -i proposal-builder-image.tar.gz
docker compose up -d
port=$(grep '^PROPOSAL_BUILDER_PORT=' .env | cut -d= -f2)
echo "Proposal Builder is starting on http://$(hostname -I 2>/dev/null | awk '{print $1}'):${port:-8501}"
