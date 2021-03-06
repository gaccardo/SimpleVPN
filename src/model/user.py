from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint, \
    Boolean, Enum

from model import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False)
    fullname = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False)
    __table_args__ = (
        UniqueConstraint("username"),
    )

    def __init__(self, username, email, fullname=None):
        self.username = username
        self.email = email
        self.fullname = fullname

    def __repr__(self):
        return "User(id={}, username={})".format(
            self.id, self.username
        )
