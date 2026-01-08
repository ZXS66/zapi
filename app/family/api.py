from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..pg import get_db
from .models import (
    FamilyMember,
    FamilyMemberCreate,
    FamilyMemberSchema,
    FamilyMemberUpdate,
    QueryRequestForm,
)

router = APIRouter()


@router.get("/members/", response_model=List[FamilyMemberSchema])
def query_list(rq: QueryRequestForm, db: Session = Depends(get_db)):
    """Query family members with pagination and search term"""
    print(f"[form data] q:{rq.q}, page_size:{rq.page_size}, page_index:{rq.page_index}")
    try:
        return (
            db.query(FamilyMember)
            .filter(FamilyMember.name.contains(rq.q))
            .offset(rq.page_size * rq.page_index)
            .limit(rq.page_size)
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


@router.put("/members/{member_id}", response_model=FamilyMemberSchema)
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
