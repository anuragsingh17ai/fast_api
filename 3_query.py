from fastapi import FastAPI
from enum import Enum

app=FastAPI()
class Model(str,Enum):
    name='anurag'

@app.get('/')
async def hello(id:int |None=None, name:Model | None=None):
    return {'id':id,'name':name}