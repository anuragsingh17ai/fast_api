from datetime import timedelta, datetime  # Used for working with time durations and dates/times
from typing import Annotated  # Helps with specifying types and adding extra information for type checking
from fastapi import APIRouter, Depends, HTTPException  # APIRouter is for creating API routes, Depends is for handling dependencies, HTTPException is for creating error responses
from pydantic import BaseModel  # BaseModel is used to define data models and validate data easily
from sqlalchemy.orm import Session  # Session is used to interact with the database in an organized way
from starlette import status  # Provides easy access to HTTP status codes like 404, 200, etc.
from databases import SessionLocal  # SessionLocal is used to create a new database session for each request
from models import Users  # Importing the User model to work with user data in the database
from passlib.context import CryptContext  # CryptContext is used for securely hashing and verifying passwords
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer  # OAuth2PasswordRequestForm helps handle login data, OAuth2PasswordBearer is for secure token authentication
from jose import jwt, JWTError  # Used for creating and verifying JSON Web Tokens (JWTs), JWTError is for handling errors with JWTs


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = '123kkk456jjj120knkvnjhfee889999kjjfkl'  # A secret key used to create and verify tokens, keep this safe and private
ALGORITHM = "HS256"  # The method used to securely sign the tokens

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")  # Set up for hashing and verifying passwords securely using bcrypt
auth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')  # Defines the token URL for users to log in and get a token to prove their identity

class CreateUserRequest(BaseModel):
    username: str 
    password: str

class Token(BaseModel):
    access_token: str 
    token_type: str 

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close

db_depenedency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_depenedency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_acess_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: db_depenedency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"acess_token": token, "token_type":"bearer"}


def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user 

def create_access_token(username: str, user_id:int, expires_delta: timedelta):
    encode = {"sub": username, "id":user_id}
    expires = datetime.utcnow + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(auth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
        return {"username": username, "id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user.")
    
    