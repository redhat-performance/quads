from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from quads.server.models import Role, Base, db
from quads.server.app import user_datastore
from quads.server import app

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def init_db():

    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()

    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)
    db.init_app(app)


def drop_all():

    Base.metadata.drop_all(bind=Engine)
