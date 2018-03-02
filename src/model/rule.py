import re

# import iptc
from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint, \
    Boolean, Enum, ForeignKey
from flask_restplus import errors

from model import Base


# class NotValidCIDR(Exception):
#
#     def __str__(self):
#         return "This is not a valid CIDR"


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
        self.proto = proto
        self.iptables = self.__as_iptables_object()
        self.set_cidr(cidr)

    def __repr__(self):
        return "Rule(name={}, port={}, p_id={}, cidr={}, proto={})".format(
            self.name, self.port, self.profile_id, self.cidr, self.proto
        )

    def as_iptables(self):
        return "-p {} -d {} --dport {} -j ACCEPT".format(
            self.proto, self.cidr, self.port)

    def __as_iptables_object(self):
        # rule = iptc.Rule()
        # rule.dst = self.cidr
        # rule.protocol = self.proto
        # match = iptc.Match(rule, self.proto)
        # match.dport = self.port
        # rule.add_match(match)
        # return rule
        return None

    def set_cidr(self, cidr):
        regexp = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)"
        if re.match(regexp, cidr) is not None:
            self.cidr = cidr
        else:
            errors.abort(
                code=400, message="{} is not a valid cidr".format(cidr)
            )
