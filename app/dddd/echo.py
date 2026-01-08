from fastapi import APIRouter, Depends

# from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..pg import get_db

router = APIRouter()


## show backend database configuration
@router.get("/db-user")
def get_db_user(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT current_user;"))
    return {"db_user": result.scalar()}
