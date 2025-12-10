from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, index=True)
    stem = Column(Text, nullable=False)  # The question or concept
    answer = Column(Text, nullable=False)
    explanation = Column(Text)
    tags = Column(JSON)  # Store as list of strings
    topic = Column(String, index=True)
    created_by = Column(String)  # username or "system" for imported data
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    knowledge_point_id = Column(Integer, index=True)
    last_reviewed = Column(DateTime)
    next_review = Column(DateTime)
    review_count = Column(Integer, default=0)
    confidence_level = Column(Integer, default=0)  # 0-5 scale
    is_learned = Column(Boolean, default=False)
