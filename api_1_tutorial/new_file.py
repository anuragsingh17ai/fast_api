from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

class request(BaseModel):
    prompt: str 
    uid: str | None
    
session = {}
@app.post('/process/')
async def upload_process(uid):
    if uid:
        return {"message":"got prompt and uid both"}
    else:
        session[uid] = uuid4()
        return {"message":prompt,"session":session[uid]}
        

