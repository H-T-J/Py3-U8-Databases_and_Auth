from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Tasks
from database import get_db

router = APIRouter()


class Task(BaseModel):
    id: int | None = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=2, max_length=250)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)
    created_on: datetime = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Title of the New Task",
                "author": "Jonathan Fernandes",
                "description": "Description of the new task",
                "priority": 1,
                "complete": False
            }
        }


# def create_id(task: Task):
#     task.id = 1 if len(TASKS) < 1 else TASKS[-1].id + 1
#     return task


# TASKS = [
#     Task(**{
#         "id": 1,
#         "title": "Unit 8",
#         "description": "In order to create more robust API's, we need to finish teaching Unit 8",
#         "author": "Jonathan Fernandes",
#         "priority": 5,
#         "complete": False
#     }),
#     Task(**{
#         "id": 2,
#         "title": "Buy Flowers",
#         "description": "Since Mrs. Fernandes has been so mean to her students, I will try to cheer her up",
#         "author": "Jonathan Fernandes",
#         "priority": 2,
#         "complete": False
#     })
# ]


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Tasks).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: Task, db: Session = Depends(get_db)):
    new_task = Task(**task_data.model_dump())

    db.add(new_task)
    db.commit()


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(task_id == Tasks.id).first()
    if task is not None:
        return task

    raise HTTPException(status_code=404, detail=f"Task with id#{task_id} not found")

@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task_by_id(task_id: int, task_data: Task, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(task_id == Tasks.id).first()

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id#{task_id} not found")

    task.title = task_data.title
    task.author = task_data.author
    task.description = task_data.description
    task.priority = task_data.priority
    task.complete = task_data.complete

    db.add(task)
    db.commit()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    delete_task = db.query(Tasks).filter(Tasks.id == task_id).first()

    if delete_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id#{task_id} not found")

    db.query(Tasks).filter(Tasks.id == task_id).delete()
    db.commit