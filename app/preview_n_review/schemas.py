from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class KnowledgePointBase(BaseModel):
    stem: str
    answer: str
    explanation: Optional[str] = None
    tags: List[str] = []
    topic: str


class KnowledgePointCreate(KnowledgePointBase):
    pass


class KnowledgePointUpdate(BaseModel):
    stem: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    topic: Optional[str] = None


class KnowledgePoint(KnowledgePointBase):
    id: int
    created_by: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str


class User(BaseModel):
    id: int
    username: str
    token: str
    created_at: datetime

    class Config:
        orm_mode = True


class ReviewSession(BaseModel):
    knowledge_points: List[KnowledgePoint]
    session_type: str  # "preview" or "review"
