from quads.server.models import db


def create_db():
    """Creates the db tables."""
    db.create_all()


def drop_db():
    """Drops the db tables."""
    db.drop_all()
