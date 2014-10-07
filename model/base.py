from sqlalchemy.ext.declarative import declarative_base
from config import metadata

Base = declarative_base(metadata=metadata)
