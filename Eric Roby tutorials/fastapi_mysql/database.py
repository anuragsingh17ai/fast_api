from fastapi import FastAPI 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

URL_DATABASE = ""

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind= engine)
Base = declarative_base()