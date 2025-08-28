FROM python:3.13-slim-bullseye

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app

# 使用阿里云镜像源
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
# 或清华大学镜像源
# ENV UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple/

# RUN uv sync --locked --no-cache
RUN uv sync

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]
