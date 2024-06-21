from fastapi import FastAPI
app=FastAPI()

@app.get('/') ##used by frontend to retrieve data from backend...
def hello():
    return {'id':1}