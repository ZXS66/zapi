from typing import Annotated
from fastapi import Header, HTTPException
from .constants import ZAPI_TOKEN

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != ZAPI_TOKEN:
        raise HTTPException(status_code=403, detail="X-Token header invalid")
