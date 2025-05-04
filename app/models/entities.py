from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Hello(Base):
    __tablename__ = "hello"

    id = Column(Integer, primary_key=True)
    text = Column(String)
