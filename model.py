""""Definition of all tables
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from config import metadata

Base = declarative_base(metadata=metadata)

class Cities(Base):
    """Cities Table"""
    __tablename__       = 'cities'

    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))


class Countries(Base):
    """Countries Table"""
    __tablename__       = 'countries'

    gid                 = sa.Column(sa.Integer, primary_key=True)
    name                = sa.Column(sa.String(100))