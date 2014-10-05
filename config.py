from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

DB_NAME = "sqla_demo"
DB_USER = "demo0"
DB_PASS = "demo"
DB_HOST = "localhost"
DB_PORT = 9241
DB_TEMPLATE = "template_postgis"
db_config = dict(driver="postgresql", host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, template=DB_TEMPLATE)

# an Engine, which the Session will use for connection
connection_string = '{driver}://{user}:{password}@{host}:{port}/{database}'.format(**db_config)
print connection_string
engine = create_engine(connection_string, pool_recycle=1, echo=True)

# create a configured "Session" class
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

metadata = MetaData()

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



