from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=-1,lt=11)

BOOKS: List[Book]= []

@app.get('/{name}', status_code= status.HTTP_200_OK)
def read_api_with_name(name):
    return {"Welcome":name}

@app.get('/', status_code= status.HTTP_200_OK)
def read_api(db: Session= Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: Book, db: Session=Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author 
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put("/update/{book_id}")
def update_book(book_id: int, book:Book, db: Session= Depends(get_db)):
    book_model = db.query(models.Books).filter(models)
    if book_model is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"ID {book_id} : Does not exist")
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()

    return book


@app.delete("/{book_id}")
def delete_book(book_id: int , db:Session=Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID : {book_id} Does not exist"
                            )
    
    db.query(models.Books).filter(models.Books.id==book_id).delete()
    db.commit()





