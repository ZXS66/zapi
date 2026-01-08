from pydantic import BaseModel
from sqlalchemy import (
    VARCHAR,
    # Boolean,
    Column,
    Date,
    # DateTime,
    Integer,
    # JSON,
    SmallInteger,
    # String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FamilyMember(Base):
    __tablename__ = "family_member"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), nullable=False)
    gender = Column(SmallInteger, nullable=False)
    father_id = Column(Integer, nullable=False)
    mother_id = Column(Integer, nullable=False)
    pin_yin = Column(Text, nullable=False)
    birthday = Column(Date)
    deathday = Column(Date)
    avatar_url = Column(Text)
    summary = Column(Text)
    extra = Column(Text)
    protected_info = Column(Text)


class QueryRequestForm(BaseModel):
    """common request form for querying"""

    q: str = ""
    """search term"""
    page_size: int = 20
    page_index: int = 0
