from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from quads.models import Base

SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost:5432/quads"
ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.bind = ENGINE
Session = sessionmaker(bind=ENGINE)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    if not database_exists(ENGINE.url):
        create_database(ENGINE.url)
    Base.metadata.create_all(ENGINE)
