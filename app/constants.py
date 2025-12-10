import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

# should set RUN_MODE environment variable via `export` before reading .env or .env.dev file
RUN_MODE = os.getenv("RUN_MODE") or "UNKNOWN"
"""current application running mode, can be 'prod' or 'dev'"""

IS_PROD_MODE = RUN_MODE == "prod"
"""detect current application is running in production mode"""

print(f"ℹ️ RUN_MODE={RUN_MODE}, IS_PROD_MODE={IS_PROD_MODE}")
_ = load_dotenv(dotenv_path=Path(".env" if IS_PROD_MODE else ".env.dev"), override=True)

# PostgreSQL Configuration
POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB") or "zapi"
POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD") or "postgres"
POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST") or "localhost"
POSTGRES_PORT: Final[str] = os.getenv("POSTGRES_PORT") or "5432"

# Application Settings
ZAPI_BASE_URL: Final[str] = os.getenv("ZAPI_BASE_URL") or "/api/"
ZAPI_TOKEN: Final[str] = os.getenv("ZAPI_TOKEN") or ""

AMAP_APP_KEY: Final[str] = os.getenv("AMAP_APP_KEY") or ""
AMAP_APP_SECRET: Final[str] = os.getenv("AMAP_APP_SECRET") or ""

WECHAT_APPID: Final[str] = os.getenv("WECHAT_APPID") or ""
WECHAT_APPSECRET: Final[str] = os.getenv("WECHAT_APPSECRET") or ""
WECHAT_TEMPLATEID: Final[str] = os.getenv("WECHAT_TEMPLATEID") or ""
WECHAT_TOUSERS: Final[list[str]] = (os.getenv("WECHAT_TOUSERS") or "").split(",")
