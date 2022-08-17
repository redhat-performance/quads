from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(
    "postgresql://postgres@localhost:5432/quads", convert_unicode=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from quads import models

    if not database_exists(engine.url):
        create_database(engine.url)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
