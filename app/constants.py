from dotenv import load_dotenv
import os

load_dotenv()

ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL") or "/api/"
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN") or ""

AMAP_APP_KEY = os.getenv("AMAP_APP_KEY") or ""
AMAP_APP_SECRET = os.getenv("AMAP_APP_SECRET") or ""
