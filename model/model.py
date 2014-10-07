""""Definition of all tables
"""
import sqlalchemy as sa
import geoalchemy as ga
from common import serialize
from base import Base


class Cities(Base):
    """Model for cities table"""

    __tablename__       = u'cities'

    # Note, all models MUST have primary key column
    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))

    #example how to map column name to variable name that is different
    country             = sa.Column("sov0name", sa.String(100))
    geom                = ga.GeometryColumn(ga.Geometry(2))

    def get_as_dict(self, depth=1):
        """Return instance as Python dictionary that is JSON serializable (easy to return in flask api)"""
        return serialize.get_as_dict(self, depth=depth)



class Countries(Base):
    """Model for countries table"""
    
    __tablename__       = u'countries'

    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))

    # Example how to map geometry column:
    geom                = ga.GeometryColumn(ga.Geometry(2))

    def get_as_dict(self, depth=1):
        return serialize.get_as_dict(self, depth=depth)