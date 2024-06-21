from fastapi import FastAPI
from enum import Enum

app=FastAPI()

class Model(str,Enum):
    name1='anurag'
    name2='adarsh'



@app.get('/{k}')
def hello(k : Model ):
    if Model.name1==k:
        return 'Hy i am anurag'
    
    return {'id':k}