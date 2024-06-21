from fastapi import APIRouter, Body

router = APIRouter()

BOOKS = [
    {"title": "Sapiens", "genre": "self help", "author": "Yuval Noah Harari"},
    {"title": "You Owe You", "genre": "self help", "author": "Eric Thomas"},
    {"title": "HC Verma", "genre": "physics", "author": "HC Verma"},
    {"title": "Rensic Halliday Walker", "genre": "physics", "author": "Halliday"},
]


@router.get("/books")
async def all_books():
    return BOOKS


@router.get("/books/genre/")  #query parameter
async def get_books_with_genre(genre: str):
    book_with_genre = []
    for book in BOOKS:
        if book.get("genre").casefold() == genre.casefold():
            book_with_genre.append(book)
    return book_with_genre


@router.post("/books/add/book/")
async def get_add_new_book(book=Body()):
    BOOKS.append(book)


@router.put("/books/update/")
async def get_update_book(book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book["title"].casefold():
            BOOKS[i] = book


@router.delete("/books/delete/")
async def delete_book(book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == book['title'].casefold():
           BOOKS.pop(i)
