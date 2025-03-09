#!/bin/bash

CONTAINER_NAME="cv_builder"
IMAGE_NAME="ghcr.io/nkyriazis/cv_builder:latest"

# Check if the container is running
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
        # Cleanup
        docker rm $CONTAINER_NAME
    fi
    # Run the container in an endless loop
    docker run -d --name $CONTAINER_NAME -v "$(pwd)":/workspace --entrypoint tail $IMAGE_NAME -f /dev/null
fi

# Execute the given command in the container
if [ -t 1 ]; then
    docker exec -it $CONTAINER_NAME "$@"
else
    docker exec $CONTAINER_NAME "$@"
fi
