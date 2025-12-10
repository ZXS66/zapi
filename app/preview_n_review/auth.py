from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from . import crud, database

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db),
):
    token = credentials.credentials
    user = crud.get_user_by_token(db, token=token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return user
