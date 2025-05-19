#!/bin/bash

IMAGE_NAME="quadbot"
TAG="latest"
GIT_REPO="https://github.com/Quadzet/quadbot.git"
GIT_BRANCH="master"

echo "===================================="
echo "Building Docker Image: $IMAGE_NAME:$TAG"
echo "Git Repository: $GIT_REPO"
echo "Git Branch: $GIT_BRANCH"
echo "===================================="

docker build \
  --progress=plain \
  --no-cache \
  --build-arg GIT_REPO="$GIT_REPO" \
  --build-arg GIT_BRANCH="$GIT_BRANCH" \
  -t "$IMAGE_NAME:$TAG" \
  .

if [ $? -eq 0 ]; then
  echo "===================================="
  echo "✅ Build successful!"
  echo "Image: $IMAGE_NAME:$TAG"
  echo ""
  echo "To run the container:"
  echo "docker run -d \\"
  echo "  --name my-discord-bot \\"
  echo "  -e DISCORD_TOKEN=\"your_token_here\" \\"
  echo "  -e DISCORD_GUILD=\"your_guild_here\" \\"
  echo "  $IMAGE_NAME:$TAG"
  echo "===================================="
else
  echo "===================================="
  echo "❌ Build failed!"
  echo "===================================="
  exit 1
fi
