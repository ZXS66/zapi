from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants import IS_PROD_MODE, ZAPI_BASE_URL
from .dddd import echo
from .dependencies import get_token_header
from .family import api as family_api
from .markdown import syntaxhighlighting
from .preview_n_review import main as pnr
from .weather import amap
from .wechat import sendAlert

app = FastAPI()

app.include_router(echo.router, prefix=ZAPI_BASE_URL + "dddd")  # just for test
app.include_router(
    family_api.router,
    prefix=ZAPI_BASE_URL + "family",
    dependencies=[Depends(get_token_header)],
)
app.include_router(
    syntaxhighlighting.router,
    prefix=ZAPI_BASE_URL + "markdown",
    dependencies=[Depends(get_token_header)],
)
app.include_router(
    pnr.router,
    prefix=ZAPI_BASE_URL + "preview-review",
    dependencies=[Depends(get_token_header)],
)
app.include_router(amap.router, prefix=ZAPI_BASE_URL + "weather")
app.include_router(
    sendAlert.router,
    prefix=ZAPI_BASE_URL + "wechat",
    dependencies=[Depends(get_token_header)],
)

if not IS_PROD_MODE:
    origins = [
        "https://localhost:4200/",
        "https://localhost.localdomain:4200/",
        "https://lvh.me:4200/",
        "https://vite.lvh.me:4200/",
    ]
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=origins,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get(ZAPI_BASE_URL)
async def index():
    return "Hello, anonymous."
