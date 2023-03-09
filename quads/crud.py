from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quads.server.models import Base

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
