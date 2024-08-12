from fastapi import APIRouter, Depends, HTTPException, status , Path
from pydantic import BaseModel
from typing import Annotated
from models import  Todo
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dpendency = Annotated[dict, Depends(get_current_user)]

class TodoBase(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool






@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dpendency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    return db.query(Todo).filter(Todo.owner_id == user.get('id'))




@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_list(user: user_dpendency, todo_list: TodoBase,db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    todo_model = Todo(**todo_list.model_dump(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()




@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dpendency, db:db_dependency,
                      todo_request: TodoBase,
                      todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code= 404, detail="Todo not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete 





@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dpendency, db:db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    todo_model = db.query(Todo).filter(todo_id==Todo.id)\
    .filter(Todo.owner_id==user.get('id')).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")





@router.delete("/todo/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dpendency, db: db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id)\
        .filter(Todo.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).delete()

    db.commit()