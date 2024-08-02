'''
sudo apt install redis-server redis-cli redis httpx
then open two terminals in first terminal -> redis-server
                        in second terminal -> redis-cli

Now in CLI
-> set name Anurag # name variable will have anurag as value
-> get name # getting value stored in name
-> del name # deleting a key
-> exists name # check whether a key exist or not return 0 for false 1 for true
-> keys * # find all keys
-> expire name 10 # expire key in 10 s
-> setex name 10 anurag # name = Anurag will exist for 10 seconds
'''

from fastapi import FastAPI
from redis import Redis
from contextlib import asynccontextmanager
import httpx
import json


@asynccontextmanager
async def event(app:FastAPI):
    app.state.redis = Redis(host='localhost',port=6379)
    app.state.http_client = httpx.AsyncClient()
    yield
    app.state.redis.close()
    await app.state.http_client.aclose()

app = FastAPI(lifespan=event)

@app.get('/entries')
async def read_item():
    values = app.state.redis.get('entries')
    if values is None:
        response = await app.state.http_client.get("https://jsonplaceholder.typicode.com/posts")
        
        values = response.json()
        data_str = json.dumps(values)
        app.state.redis.set("entries",data_str)
    
    return json.loads(values)
