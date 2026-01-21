from datetime import date
from typing import Any, List, Optional

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
    gender = Column(SmallInteger)
    father_id = Column(Integer, default=-1, comment="父亲id，-1表示未知")
    mother_id = Column(Integer, default=-1, comment="母亲id，-1表示未知")
    pin_yin = Column(Text)
    birthday = Column(Date)
    deathday = Column(Date)
    avatar_url = Column(Text)
    summary = Column(Text)
    extra = Column(Text)
    protected_info = Column(Text)
    title = Column(VARCHAR(32), default="", comment="头衔/称谓")


class FamilyMemberBase(BaseModel):
    """Base schema for family member data"""

    name: str
    gender: Optional[int] = 0
    father_id: Optional[int] = -1
    mother_id: Optional[int] = -1
    pin_yin: Optional[str] = None
    birthday: Optional[date] = None
    deathday: Optional[date] = None
    avatar_url: Optional[str] = None
    summary: Optional[str] = None
    extra: Optional[str] = None
    protected_info: Optional[str] = None
    title: Optional[str] = None


class FamilyMemberCreate(FamilyMemberBase):
    """Schema for creating a new family member"""

    pass


class FamilyMemberUpdate(BaseModel):
    """Schema for updating a family member (all fields optional)"""

    name: Optional[str] = None
    gender: Optional[int] = None
    father_id: Optional[int] = None
    mother_id: Optional[int] = None
    pin_yin: Optional[str] = None
    birthday: Optional[date] = None
    deathday: Optional[date] = None
    avatar_url: Optional[str] = None
    summary: Optional[str] = None
    extra: Optional[str] = None
    protected_info: Optional[str] = None
    title: Optional[str] = None


class FamilyMemberSchema(FamilyMemberBase):
    """Schema for family member response (includes ID)"""

    id: int

    class Config:
        orm_mode = True


class NameValueTagSchema(BaseModel):
    name: str
    value: Any
    tag: Any = None
    """optional attribute for remark"""


class NameValueChildrenSchema(NameValueTagSchema):
    children: List["NameValueChildrenSchema"] = []
    """child nodes, empty by default"""
    # def __init__(self):
    #     self.children = []
