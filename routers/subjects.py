from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Subjects
from database import get_db

router = APIRouter()


class Subject(BaseModel):
    id: int | None = None
    name: str = Field(min_length=2)
    teacher: str = Field(min_length=3)
    description: str = Field(min_length=2, max_length=150)
    year_long: bool = Field(default=False)
    credits: str = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name of subject",
                "teacher": "primary instructor of the subject",
                "description": "brief description of the subject",
                "year_long": False,
                "credits": "2"
            }
        }



@router.get("", status_code=status.HTTP_200_OK)
async def get_subject_registry(db: Session = Depends(get_db)):

    return db.query(Subjects).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_subject(subject_data: Subject, db: Session = Depends(get_db)):

    new_subject = Subjects(**subject_data.model_dump())

    db.add(new_subject)
    db.commit()


@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def get_subject_by_id(subject_id: int, db: Session = Depends(get_db)):

    subject = db.query(Subjects).filter(subject_id == Subjects.id).first()
    if subject is not None:
        return subject

    raise HTTPException(status_code=404, detail=f"Subject with id#{subject_id} not found")

@router.put("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_subject_by_id(subject_id: int, subject_data: Subject, db: Session = Depends(get_db)):

    subject = db.query(Subjects).filter(subject_id == Subjects.id).first()

    if subject is None:
        raise HTTPException(status_code=404, detail=f"Subject with id#{subject_id} not found")

    subject.name = subject_data.name
    subject.teacher = subject_data.teacher
    subject.description = subject_data.description
    subject.year_long = subject_data.year_long

    db.add(subject)
    db.commit()


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject_by_id(subject_id: int, db: Session = Depends(get_db)):

    delete_subject = db.query(Subjects).filter(Subjects.id == subject_id).first()

    if delete_subject is None:
        raise HTTPException(status_code=404, detail=f"Subject with id#{subject_id} not found")

    db.query(Subjects).filter(Subjects.id == subject_id).delete()
    db.commit()