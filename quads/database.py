from sqlalchemy_utils import database_exists, create_database


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from quads.server.models import *

    if not database_exists(Engine.url):
        create_database(Engine.url)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=Engine)
