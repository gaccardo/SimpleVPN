from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint, \
    Boolean, Enum, ForeignKey

from model import Base


class Certificate(Base):
    __tablename__ = 'certificate'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    valid = Column(Boolean, default=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    ip = Column(String(256), nullable=True)

    def __init__(self, name, user_id, valid=True, ip=None):
        self.name = name
        self.user_id = user_id
        self.valid = valid
        self.ip = ip

    def __repr__(self):
        return "Certificate(id={}, name={})".format(
            self.id, self.name
        )
