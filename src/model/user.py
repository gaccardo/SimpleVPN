from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy import Boolean, Enum

from model import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False)
    fullname = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False)
    certificate = Column(String(256), nullable=True)
