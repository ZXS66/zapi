# zapi - API Collections for Study

A FastAPI project providing various RESTful APIs including a Knowledge Review System for spaced repetition learning.

The Knowledge Review System helps users preview knowledge points in the morning and review them in the afternoon/evening using spaced repetition.

## Available APIs

- **Preview & Review System**: Spaced repetition learning with knowledge points
- **Markdown Syntax Highlighting**: Code formatting for markdown documents
- **Weather API**: Weather information via AMap
- **WeChat Alerts**: Send notifications via WeChat

## Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to project
cd zapi

# Install dependencies using uv
uv sync

# Setup environment variables
# Create .env for production and .env.dev for development
# The DATABASE_URL will be automatically constructed from PostgreSQL components
```

### 2. Environment Configuration

Edit your environment files:

**Production (.env):**

**Development (.env.dev):**


### 3. Run the Application

**Run with uv or Uvicorn (Recommended)**
```bash
uv run fastapi run app/main.py --port 8000 --reload
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`


## API Documentation & Structure

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Base URLs
- **Preview & Review System**: `/api/preview-review/`
- **Markdown**: `/api/markdown/`
- **Weather**: `/api/weather/`
- **WeChat**: `/api/wechat/`


## Development & Package Management

### Package Management with uv

This project uses `uv` for package management. All dependencies are defined in `pyproject.toml`.

```bash
# Install dependencies
uv sync

# Add new dependency
uv add package_name

# Run with uv
uv run fastapi dev
```

## Deployment & Running

## License

MIT License - see [LICENSE](./LICENSE) file for details
