from fastapi import APIRouter, Depends, HTTPException, status , Path
from pydantic import BaseModel
from typing import Annotated
from models import  Todo
from database import SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

class TodoBase(BaseModel):
    title: str
    description: str
    priority: int

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_list(todo_list: TodoBase,db : db_dependency):
    todo_model = Todo(**todo_list.model_dump())
    db.add(todo_model)
    db.commit()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(todo_id==Todo.id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")