from .database import init_db, drop_all


def create_db():
    """Creates database"""

    init_db()


def drop_db():
    """Drop / Clean database - DANGER ACTION"""
    drop_all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
