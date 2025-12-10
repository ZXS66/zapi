
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.constants import AMAP_APP_KEY, IS_PROD_MODE
from sqlalchemy import text
from app.preview_n_review.database import engine


router = APIRouter()


@router.get("/db-user")
def get_db_user():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_user;"))
        return {"db_user": result.scalar()}
