from fastapi import FastAPI,Query
from typing import Annotated
app=FastAPI()

@app.get('/')
async def home(id:Annotated[str|None,Query()]=None):
    return {'hi':id}

@app.get('/c')
async def title(
    q:Annotated[str,Query(title='name',alias='n',deprecated=True,description='name of user',max_length=10,pattern='(\d+$)',min_length=2,)]
    ):
    return q
