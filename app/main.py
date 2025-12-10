from fastapi import Depends, FastAPI

from .constants import ZAPI_BASE_URL
from .dddd import db
from .dependencies import get_token_header
from .markdown import syntaxhighlighting
from .preview_n_review.main import router as preview_review_router
from .weather import amap
from .wechat import sendAlert

app = FastAPI()

app.include_router(
    syntaxhighlighting.router,
    prefix=ZAPI_BASE_URL + "markdown",
    dependencies=[Depends(get_token_header)],
)
app.include_router(amap.router, prefix=ZAPI_BASE_URL + "weather")
app.include_router(
    sendAlert.router,
    prefix=ZAPI_BASE_URL + "wechat",
    dependencies=[Depends(get_token_header)],
)
app.include_router(
    preview_review_router,
    prefix=ZAPI_BASE_URL + "preview-review",
    dependencies=[Depends(get_token_header)],
)
app.include_router(db.router, prefix=ZAPI_BASE_URL + "dddd")    # just for test


@app.get(ZAPI_BASE_URL)
async def index():
    return "Hello, anonymous."
