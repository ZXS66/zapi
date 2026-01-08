from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    import secrets

    token = secrets.token_urlsafe(32)
    db_user = models.User(username=user.username, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_knowledge_point(
    db: Session, knowledge_point: schemas.KnowledgePointCreate, username: str
):
    db_kp = models.KnowledgePoint(
        stem=knowledge_point.stem,
        answer=knowledge_point.answer,
        explanation=knowledge_point.explanation,
        tags=knowledge_point.tags,
        topic=knowledge_point.topic,
        created_by=username,
    )
    db.add(db_kp)
    db.commit()
    db.refresh(db_kp)
    return db_kp


def get_knowledge_points_for_preview(db: Session, user_id: int, limit: int = 5):
    # Get knowledge points that haven't been reviewed today
    today = datetime.now().date()
    return (
        db.query(models.KnowledgePoint)
        .outerjoin(
            models.UserProgress,
            (models.UserProgress.knowledge_point_id == models.KnowledgePoint.id)
            & (models.UserProgress.user_id == user_id),
        )
        .filter(
            (models.UserProgress.last_reviewed.is_(None))
            | (models.UserProgress.last_reviewed < today)
        )
        .filter(models.KnowledgePoint.is_active.is_(True))
        .limit(limit)
        .all()
    )


def get_knowledge_points_for_review(db: Session, user_id: int, limit: int = 5):
    # Get knowledge points that were previously seen and need reinforcement
    today = datetime.now().date()
    return (
        db.query(models.KnowledgePoint)
        .join(
            models.UserProgress,
            (models.UserProgress.knowledge_point_id == models.KnowledgePoint.id)
            & (models.UserProgress.user_id == user_id),
        )
        .filter(
            models.UserProgress.last_reviewed < today,
            models.KnowledgePoint.is_active.is_(True),
        )
        .order_by(models.UserProgress.confidence_level.asc())
        .limit(limit)
        .all()
    )


def search_knowledge_points(
    db: Session, query: Optional[str] = None, tags: Optional[List[str]] = None
):
    search_query = db.query(models.KnowledgePoint).filter(
        models.KnowledgePoint.is_active.is_(True)
    )

    if query:
        search_query = search_query.filter(
            models.KnowledgePoint.stem.ilike(f"%{query}%")
            | models.KnowledgePoint.answer.ilike(f"%{query}%")
            | models.KnowledgePoint.topic.ilike(f"%{query}%")
            | models.KnowledgePoint.explanation.ilike(f"%{query}%")
        )

    if tags:
        search_query = search_query.filter(models.KnowledgePoint.tags.contains(tags))

    return search_query.all()


def record_user_progress(
    db: Session, user_id: int, knowledge_point_id: int, confidence_level: int
):
    # Find existing progress record
    progress = (
        db.query(models.UserProgress)
        .filter(
            models.UserProgress.user_id == user_id,
            models.UserProgress.knowledge_point_id == knowledge_point_id,
        )
        .first()
    )

    if progress:
        # Update existing progress
        progress.last_reviewed = datetime.now()  # type: ignore
        progress.review_count += 1  # type: ignore
        progress.confidence_level = confidence_level  # type: ignore

        # Calculate next review based on confidence (spaced repetition)
        if confidence_level >= 4:
            progress.is_learned = True  # type: ignore
            progress.next_review = datetime.now() + timedelta(  # type: ignore
                days=7
            )  # Review in 1 week
        elif confidence_level >= 2:
            progress.next_review = datetime.now() + timedelta(  # type: ignore
                days=3
            )  # Review in 3 days
        else:
            progress.next_review = datetime.now() + timedelta(  # type: ignore
                days=1
            )  # Review tomorrow
    else:
        # Create new progress record
        progress = models.UserProgress(
            user_id=user_id,
            knowledge_point_id=knowledge_point_id,
            last_reviewed=datetime.now(),
            review_count=1,
            confidence_level=confidence_level,
        )

        # Set next review based on confidence
        if confidence_level >= 4:
            progress.is_learned = True  # type: ignore
            progress.next_review = datetime.now() + timedelta(days=7)  # type: ignore
        elif confidence_level >= 2:
            progress.next_review = datetime.now() + timedelta(days=3)  # type: ignore
        else:
            progress.next_review = datetime.now() + timedelta(days=1)  # type: ignore

        db.add(progress)

    db.commit()
    db.refresh(progress)
    return progress


def get_user_knowledge_points(db: Session, username: str):
    return (
        db.query(models.KnowledgePoint)
        .filter(
            models.KnowledgePoint.created_by == username,
            models.KnowledgePoint.is_active.is_(True),
        )
        .all()
    )
