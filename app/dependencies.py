from typing import Annotated
from fastapi import Header, HTTPException, Query
from .constants import ZAPI_TOKEN

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != ZAPI_TOKEN:
        raise HTTPException(status_code=403, detail="x-token header invalid")

async def get_token_query(x_token: Annotated[str, Query()]):
    if x_token != ZAPI_TOKEN:
        raise HTTPException(status_code=403, detail="x-token query invalid")
