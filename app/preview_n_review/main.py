from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import auth, crud, database, models, schemas
from .database import engine

# Create tables
models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# API 1: User Registration
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# API 2: Get Preview Session (Morning)
@router.get("/preview/", response_model=schemas.ReviewSession)
def get_preview_session(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
    limit: int = Query(5, description="Number of knowledge points to preview"),
):
    knowledge_points = crud.get_knowledge_points_for_preview(db, current_user.id, limit)
    return {"knowledge_points": knowledge_points, "session_type": "preview"}


# API 3: Get Review Session (Afternoon/Evening)
@router.get("/review/", response_model=schemas.ReviewSession)
def get_review_session(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
    limit: int = Query(5, description="Number of knowledge points to review"),
):
    # For review, get items that were previously seen and need reinforcement
    knowledge_points = crud.get_knowledge_points_for_review(db, current_user.id, limit)
    return {"knowledge_points": knowledge_points, "session_type": "review"}


# API 4: Search Knowledge Points
@router.get("/knowledge-points/search/", response_model=List[schemas.KnowledgePoint])
def search_knowledge_points(
    query: Optional[str] = Query(None, description="Search in stem, answer, and topic"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.search_knowledge_points(db, query, tags)


# API 5: Create Knowledge Point
@router.post("/knowledge-points/", response_model=schemas.KnowledgePoint)
def create_knowledge_point(
    knowledge_point: schemas.KnowledgePointCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.create_knowledge_point(db, knowledge_point, current_user.username)


# API 6: Import Knowledge Points (Batch)
@router.post("/knowledge-points/import/")
def import_knowledge_points(
    knowledge_points: List[schemas.KnowledgePointCreate],
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    imported = []
    for kp in knowledge_points:
        db_kp = crud.create_knowledge_point(db, kp, current_user.username)
        imported.append(db_kp)
    return {"imported_count": len(imported), "knowledge_points": imported}


# API 7: Export Knowledge Points
@router.get("/knowledge-points/export/")
def export_knowledge_points(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    knowledge_points = crud.get_user_knowledge_points(db, current_user.username)

    export_data = [
        {
            "stem": kp.stem,
            "answer": kp.answer,
            "explanation": kp.explanation,
            "tags": kp.tags,
            "topic": kp.topic,
        }
        for kp in knowledge_points
    ]

    return {"export_data": export_data}


# API 8: Record Review Progress
@router.post("/progress/")
def record_progress(
    knowledge_point_id: int,
    confidence_level: int = Query(..., ge=0, le=5, description="Confidence level 0-5"),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.record_user_progress(
        db, current_user.id, knowledge_point_id, confidence_level
    )


# API 9: Get User's Knowledge Points
@router.get("/knowledge-points/", response_model=List[schemas.KnowledgePoint])
def get_user_knowledge_points(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db),
):
    return crud.get_user_knowledge_points(db, current_user.username)


# Root endpoint for preview-review module
@router.get("/")
async def root():
    return {"message": "Knowledge Review System", "version": "1.0.0"}
