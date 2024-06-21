from fastapi import FastAPI
from books2.routers.books import router as books_router
app = FastAPI()

app.include_router(books_router)