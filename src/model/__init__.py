
from sqlalchemy.ext import declarative

declarative_base = lambda cls: declarative.declarative_base(cls=cls)

@declarative_base
class Base(object):
    __table_args__ = {'mysql_engine': 'InnoDB'}
