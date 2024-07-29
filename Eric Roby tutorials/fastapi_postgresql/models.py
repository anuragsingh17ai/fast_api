from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from databases import Base

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = "choice"

    id = Column(Integer, primary_key=True, index= True)
    choices_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    