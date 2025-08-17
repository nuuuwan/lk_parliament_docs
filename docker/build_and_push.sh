#!/usr/bin/env bash
set -euo pipefail

docker --version
URL=ghcr.io/nuuuwan/lk-acts-image:latest
echo "URL=$URL"

# Make builder idempotent
docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
  docker buildx create --name multiarch-builder --use
docker buildx use multiarch-builder

# Make sure you’re logged in (uncomment the next line or ensure GHCR login elsewhere)
# echo "$GITHUB_TOKEN" | docker login ghcr.io -u nuuuwan --password-stdin

docker buildx build \
  -f docker/Dockerfile \
  --platform linux/amd64,linux/arm64 \
  -t "$URL" \
  --push \
  .

echo 'Validating Python Version...'
docker run --rm "$URL" python --version
echo 'Done!'

open https://github.com/nuuuwan?tab=packages