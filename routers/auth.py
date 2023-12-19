from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Users
from database import get_db

router = APIRouter()


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    alt_name: str = Field(min_length=2)
    email: str = Field(min_length=2, max_length=250)
    password: int = Field(lt=20)
    role: str = Field(min_length=2, max_length=20)


    class Config:
        json_schema_extra = {
            "example": {
                "name": "name of user",
                "alt_name": "alternative name",
                "email": "email used to log in",
                "password": "password used to log in",
                "role": "role, if student leave blank",
                }
            }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = UserCreate(**user_data.model_dump())

    db.add(new_user)
    db.commit()