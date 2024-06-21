from contextlib import asynccontextmanager


from fastapi import FastAPI

from api_2_socialMedia.database import database
from api_2_socialMedia.routers.post import router as post_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
