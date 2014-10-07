""""Definition of all tables
"""
import sqlalchemy as sa
import geoalchemy as ga
from common import serialize
from base import Base


class Cities(Base):
    """Cities Table"""
    __tablename__       = 'cities'

    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))
    country             = sa.Column("sov0name", sa.String(100))
    #geom                = ga.GeometryColumn(ga.Geometry(2))

    def get_as_dict(self, depth=1):
        return serialize.get_as_dict(self, depth=depth)



class Countries(Base):
    """Countries Table"""
    __tablename__       = 'countries'

    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))

    def get_as_dict(self, depth=1):
        return serialize.get_as_dict(self, depth=depth)