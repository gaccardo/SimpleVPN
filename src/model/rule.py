from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint, \
    Boolean, Enum, ForeignKey

from model import Base


class Rule(Base):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=True)
    cidr = Column(String(256), nullable=True, default="0.0.0.0/0")
    proto = Column(String(256), nullable=True, default="tcp")
    port = Column(String(256), nullable=False)
    profile_id = Column(ForeignKey("profile.id"), nullable=False)

    def __init__(self, port, profile_id, name=None, cidr="0.0.0.0/0",
                 proto="tcp"):
        self.port = port
        self.profile_id = profile_id
        self.name = name
        self.cidr = cidr
        self.proto = proto

    def __repr__(self):
        return "Rule(name={}, port={}, p_id={}, cidr={}, proto={})".format(
            self.name, self.port, self.profile_id, self.cidr, self.proto
        )

    def as_iptables(self):
        return "-p {} -d {} --dport {} -j ACCEPT".format(
            self.proto, self.cidr, self.port)
