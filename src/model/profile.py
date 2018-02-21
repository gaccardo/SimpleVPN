from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint, \
    Boolean, Enum

from model import Base


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    __table_args__ = (
        UniqueConstraint("name"),
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Profile(name={})".format(self.name)
