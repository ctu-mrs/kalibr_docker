xhost +local:docker

docker compose -f "$(dirname "$0")/compose.yaml" up --attach-dependencies

xhost -local:docker
