from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

router = APIRouter()


class Books:
    id: int
    title: str
    description: str
    author: str
    rating: str
    release_date: str

    def __init__(self, id, title, description, author, rating, release_date) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating
        self.release_date = release_date


class Validate_book(BaseModel):
    id: Optional[int] = Field(None, description="This is not manditory")
    title: str = Field(..., min_length=1, description="This is the title of the book")
    description: str = Field(..., min_length=4, max_length=50)
    author: str = Field(..., description="Name of the author of book")
    rating: int = Field(gt=-1, lt=6)
    release_date: str = Field(..., description="this is the release date of book")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "python greats",
                    "description": "best thing about python",
                    "author": "Anurag Singh",
                    "rating": 5,
                    "release_date": "22/04/2024",
                }
            ]
        }
    }


BOOKS = [
    Books(
        1, "python tutorials", "This is all about Python", "Anurag Singh", 5, "22/05/24"
    )
]


@router.get("/books/all", status_code=status.HTTP_200_OK)
async def all_books():
    return BOOKS


@router.get("/books/find/id/{id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(id: int):
    for i in BOOKS:
        if i.id == id:
            return i

    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/books/find/rating/", status_code=status.HTTP_200_OK)
async def find_book_by_rating(rating: int = Query(gt=-1, lt=6)):
    filter_book = []
    for i in BOOKS:
        if i.rating == rating:
            filter_book.append(i)

    if len(filter_book) == 0:
        return "No Book Found!"

    return filter_book


@router.post("/books/add/", status_code=status.HTTP_201_CREATED)
async def add_book(book: Validate_book):
    new_book = Books(**book.model_dump())
    BOOKS.append(find_book_id(new_book))


@router.put("/books/update_book/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: Validate_book, id: int = Path(gt=-1)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS[i] = book
            BOOKS[i].id = id
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail="book not found!")


@router.delete("/books/delete/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="book not found")


def find_book_id(book: Books):

    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book
