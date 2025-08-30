from dotenv import load_dotenv
import os
from typing import Final, List

load_dotenv()

ZAPI_BASE_URL: Final[str] = os.getenv("ZAPI_BASE_URL") or "/api/"
ZAPI_TOKEN: Final[str] = os.getenv("ZAPI_TOKEN") or ""

AMAP_APP_KEY: Final[str] = os.getenv("AMAP_APP_KEY") or ""
AMAP_APP_SECRET: Final[str] = os.getenv("AMAP_APP_SECRET") or ""

WECHAT_APPID: Final[str] = os.getenv("WECHAT_APPID") or ""
WECHAT_APPSECRET: Final[str] = os.getenv("WECHAT_APPSECRET") or ""
WECHAT_TEMPLATEID: Final[str] = os.getenv("WECHAT_TEMPLATEID") or ""
WECHAT_TOUSERS: Final[List[str]] = (os.getenv("WECHAT_TOUSERS") or "").split(",")

RUN_MODE = os.getenv("RUN_MODE") or "UNKNOWN"

IS_PROD_MODE = RUN_MODE == "prod"
"""detect current application is running in production mode"""
