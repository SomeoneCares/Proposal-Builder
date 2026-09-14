#!/usr/bin/env bash
# Build the Docker image (tests run inside the build) and write a portable bundle:
#   dist/proposal-builder-<tag>.tar.gz
#     proposal-builder-image.tar.gz  the image (docker load)
#     docker-compose.yml, .env.example, start.sh, RUN.md
# Copy the bundle to any host with Docker, unpack it and run ./start.sh.
#
# Usage: scripts/package.sh [tag]      (default tag: short commit id)
set -euo pipefail

cd "$(dirname "$0")/.."
sha=$(git rev-parse --short HEAD)
tag=${1:-$sha}
image=vertowave/proposal-builder
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "== note: uncommitted changes are included in this build"
fi

echo "== building $image:$tag"
docker build --build-arg GIT_SHA="$sha" -t "$image:$tag" -t "$image:latest" .

bundle="proposal-builder-$tag"
stage="dist/$bundle"
rm -rf "$stage" && mkdir -p "$stage"
echo "== saving the image"
docker save "$image:$tag" | gzip > "$stage/proposal-builder-image.tar.gz"
cp docker-compose.yml scripts/bundle/RUN.md "$stage/"
install -m 755 scripts/bundle/start.sh "$stage/start.sh"
{ cat .env.example; printf '\n# Image tag in this bundle\nPROPOSAL_BUILDER_TAG=%s\n' "$tag"; } > "$stage/.env.example"

tar -C dist -czf "dist/$bundle.tar.gz" "$bundle"
rm -rf "$stage"
echo "== wrote dist/$bundle.tar.gz ($(du -h "dist/$bundle.tar.gz" | cut -f1))"
