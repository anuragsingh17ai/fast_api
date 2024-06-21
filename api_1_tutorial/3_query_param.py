from fastapi import FastAPI

app = FastAPI()

@app.get('/items/')
async def read_item(skip:int=0, limit:int=10, q:str|None =None, b:bool=True):
    return {skip,limit,q,b}