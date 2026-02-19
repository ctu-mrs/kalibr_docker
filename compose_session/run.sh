xhost +

docker compose -f "$(dirname "$0")/compose.yaml" up --attach-dependencies
