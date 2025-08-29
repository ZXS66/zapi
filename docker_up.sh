IMAGE_NAME="zapi"
CONTAINER_NAME="${IMAGE_NAME}_pod"

if type podman >/dev/null 2>&1; then
    # podman is preferred
    podman build -t "$IMAGE_NAME" .
    podman stop "$CONTAINER_NAME" | xargs podman rm
    podman run -itd -p 8081:80 --name "$CONTAINER_NAME" "$IMAGE_NAME"
else
    # docker as fallback
    sudo docker build -t "$IMAGE_NAME" .
    sudo docker stop "$CONTAINER_NAME" | xargs sudo docker rm
    sudo docker run -itd -p 8081:80 --name "$CONTAINER_NAME" "$IMAGE_NAME"
fi
