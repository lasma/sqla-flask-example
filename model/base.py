from sqlalchemy.ext.declarative import declarative_base
from config import metadata

# This is the base class for all models (table mappings)
Base = declarative_base(metadata=metadata)
