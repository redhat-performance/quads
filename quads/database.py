from sqlalchemy_utils import database_exists, create_database

from quads.server.models import Base, Engine, engine_from_config


def init_db(config=None):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import quads.server.models

    engine = Engine
    if config:
        engine = engine_from_config(config)

    if not database_exists(engine.url):
        create_database(engine.url)
    quads.server.models.Base.metadata.create_all(bind=engine)


def drop_db(config=None):
    engine = Engine
    if config:
        engine = engine_from_config(config)
    Base.metadata.drop_all(bind=engine)
