from fastapi import FastAPI
from pydantic import BaseModel

class Model(BaseModel):
    name:str
    description:str


app=FastAPI()
@app.post('/{i}')
async def hi(i:str,id:Model, k:int):
    print(id.name,i,k)
    

