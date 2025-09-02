from fastapi import Depends, FastAPI

from .constants import ZAPI_BASE_URL
from .dependencies import get_token_header
from .weather import amap
from .wechat import sendAlert

app = FastAPI()

app.include_router(
    amap.router,
    prefix=ZAPI_BASE_URL+"weather"
)
app.include_router(
    sendAlert.router,
    prefix=ZAPI_BASE_URL+"wechat",
    dependencies=[Depends(get_token_header)],
)

@app.get(ZAPI_BASE_URL)
async def index():
    return "Hello, anonymous."
