from database import Base 
from sqlalchemy import Integer, Column,Boolean,String, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)



class Todo(Base):
    __tablename__ = 'todo'


    id = Column(Integer, primary_key= True, index=True, autoincrement="auto")
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))