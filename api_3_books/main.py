""" This project is using simple crud operation for book library system
"""

from fastapi import FastAPI

from books.routers.books import router as book_routes

app = FastAPI()

app.include_router(book_routes)
