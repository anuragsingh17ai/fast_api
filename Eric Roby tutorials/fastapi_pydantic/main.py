# pip install email-validator

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator,EmailStr
from uuid import UUID, uuid4

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=12) 
    age: int = Field(gt=12,lt=100)

    class Config:
        json_schema_extra = {
            'example':{
                'email':"test@gmail.com",
                'password':"test123!",
                "age":65
            }
        }
    
    @field_validator('password')
    def password_validate(cls, value):
        if value == "test123!":
            raise ValueError("Please do not use default password...")
        return value
    

class User(UserCreate):
    id: UUID = Field(default_factory=uuid4)



@app.post("/users/",response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    created_user = User(**user.model_dump())
    return created_user