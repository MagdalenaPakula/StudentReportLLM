#!/bin/bash

set -euo pipefail

check_health() {
  exited_containers=$(docker ps --filter "status=exited" --format '{{.Image}}')
  if [ -n "$exited_containers" ]; then
    echo "Exited containers detected:"
    echo "$exited_containers"
    return 1
  fi
  unhealthy_containers=$(docker ps --filter "health=unhealthy" --format '{{.Image}}')
  if [ -n "$unhealthy_containers" ]; then
    echo "Unhealthy containers detected:"
    echo "$unhealthy_containers"
    return 1
  fi
  pending_containers=$(docker ps --filter "health=starting" --format '{{.Image}}')
  if [ -n "$pending_containers" ]; then
    return 2
  fi
  return 0
}

existing_containers=$(docker ps -a)
if [ -n "$existing_containers" ]; then
  echo "Existing containers detected. Please remove any containers before running this script"
  exit 1
fi

echo "Staring containers..."
docker compose up -d

MAX_RETRIES=10
RETRY_INTERVAL_SECONDS=1
for (( i = 0; i < MAX_RETRIES; i++ )); do
  echo "Checking container health. Attempt $i of $MAX_RETRIES"

  if check_health; then
    # ensure are still healthy after 3 seconds then exit with success
    sleep 3
    check_health
    exit 0
  fi

  health_status=$?
  if [ $health_status -eq 1 ]; then
    exit 1
  fi

  sleep $RETRY_INTERVAL_SECONDS
done

echo "Error: Timeout waiting for containers to become healthy."
docker compose ps -a
exit 1




