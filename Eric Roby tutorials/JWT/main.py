"""
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install python-multipart
"""
import models
from databases import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from auth import get_current_user, router

app = FastAPI()
app.include_router(router)
models.Base.metadata.create_all(bind= engine)


user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail= "Authentication Failed")
    return {"User": user}

    

