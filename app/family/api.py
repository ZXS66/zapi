from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.pg import get_db

from .models import FamilyMember, QueryRequestForm

router = APIRouter()


@router.post("/list")
def query_list(rq: QueryRequestForm, db: Session = Depends(get_db)):
    print(f"[form data] q:{rq.q}, page_size:{rq.page_size}, page_index:{rq.page_index}")
    # return db.query(FamilyMember).all()
    return (
        db.query(FamilyMember)
        .filter(FamilyMember.name.contains(rq.q))
        .offset(rq.page_size * rq.page_index)
        .limit(rq.page_size)
        .all()
    )
