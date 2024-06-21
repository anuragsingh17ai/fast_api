from fastapi import FastAPI

app = FastAPI()

@app.get('/items/{id}')
async def read_id(id:int):
    return {'item id': id}