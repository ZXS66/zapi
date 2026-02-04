from fastapi import APIRouter, Depends, HTTPException
from json import loads
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Any, List, Optional, Tuple

from ..pg import get_db
from .models import (
    FamilyMember,
    FamilyMemberCreate,
    FamilyMemberSchema,
    FamilyMemberUpdate,
    NameValueChildrenSchema,
    NameValueTagSchema,
)

router = APIRouter()


@router.get("/members/", response_model=List[FamilyMemberSchema])
def query_list(
    q: Optional[str] = None,
    page_size: Optional[int] = None,
    page_index: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Query family members with pagination and search term"""
    print(f"[form data] q:{q}, page_size:{page_size}, page_index:{page_index}")
    if not q:
        q = ""
    if not page_size:
        page_size = 10
    if not page_index:
        page_index = 0
    try:
        return (
            db.query(FamilyMember)
            .filter(FamilyMember.name.contains(q))
            .order_by(FamilyMember.id.asc())
            .offset(page_size * page_index)
            .limit(page_size)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")


@router.post("/members/", response_model=FamilyMemberSchema)
def create_member(
    member: FamilyMemberCreate, db: Session = Depends(get_db)
) -> FamilyMemberSchema:
    """Create a new family member"""
    try:
        db_member = FamilyMember(**member.model_dump())
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Database integrity error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/members/bulk/", response_model=List[FamilyMemberSchema])
def bulk_create_members(
    members: List[FamilyMemberCreate], db: Session = Depends(get_db)
) -> List[FamilyMemberSchema]:
    """Bulk insert multiple family members"""
    db_members = []
    try:
        for member in members:
            db_member = FamilyMember(**member.model_dump())
            db.add(db_member)
            db_members.append(db_member)
        db.commit()
        # Refresh each member to get IDs
        for db_member in db_members:
            db.refresh(db_member)
        return db_members
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Database integrity error in bulk insert: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Internal server error in bulk insert: {str(e)}"
        )


@router.get("/members/{member_id}", response_model=FamilyMemberSchema)
def get_member(member_id: int, db: Session = Depends(get_db)) -> FamilyMemberSchema:
    """Retrieve a single family member by ID"""
    db_member = db.query(FamilyMember).filter(FamilyMember.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Family member not found")
    return db_member


@router.post("/members/{member_id}", response_model=FamilyMemberSchema)
def update_member(
    member_id: int, member_update: FamilyMemberUpdate, db: Session = Depends(get_db)
) -> FamilyMemberSchema:
    """Update an existing family member"""
    db_member = db.query(FamilyMember).filter(FamilyMember.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Family member not found")

    # Update only provided fields
    update_data = member_update.model_dump(exclude_unset=True)
    try:
        for field, value in update_data.items():
            setattr(db_member, field, value)
        db.commit()
        db.refresh(db_member)
        return db_member
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Database integrity error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/namemeta/", response_model=List[NameValueTagSchema])
def query_namemeta(
    db: Session = Depends(get_db),
):
    """Query metadata of id-name pairs"""
    try:
        return db.query(
            FamilyMember.id.label("value"),
            FamilyMember.name,
            FamilyMember.gender.label("tag"),
        ).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")


@router.get("/hierarchy/", response_model=Optional[NameValueChildrenSchema])
def query_hierarchy(
    db: Session = Depends(get_db),
) -> Optional[NameValueChildrenSchema]:
    """Query all members in hierarchy (nested) structure, discard isolated members (no connection to the root member)"""
    """assumption: no cycle reference(s)"""
    try:
        data = db.query(
            FamilyMember.id,
            FamilyMember.name,
            FamilyMember.father_id,
            FamilyMember.title,
            FamilyMember.birthday
        ).order_by(FamilyMember.birthday).all()
        if data is None or len(data) == 0:
            return None
        mapping = {d[0]: _parseNameValueChildrenSchema(d) for d in data}
        for d in data:
            if d.father_id in mapping:
                child = mapping[d.id]
                mapping[d.father_id].children.append(child)
        return mapping[1]  # root node's id equals to 1, and should alwarys exist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")


def _parseNameValueChildrenSchema(data: Any) -> NameValueChildrenSchema:
    id, name, _, title, _ = data
    return NameValueChildrenSchema(
        name=name,
        value=id,
        # tag=loads(extra) if extra and len(extra)>0 else None
        tag=title,
    )
