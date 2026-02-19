docker compose -f "$(dirname "$0")/compose.yaml" down --remove-orphans
docker network prune -f
