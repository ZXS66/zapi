IMAGE_NAME="zapi"

if type podman >/dev/null 2>&1; then
    podman build -t "$IMAGE_NAME" .
    podman run -itd -p 8081:80 "$IMAGE_NAME"
else
    sudo docker build -t "$IMAGE_NAME" .
    sudo docker run -itd -p 8081:80 "$IMAGE_NAME"
fi
