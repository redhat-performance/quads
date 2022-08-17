from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from quads.models import Role
from quads.server.app import user_datastore

Engine = create_engine(
    "postgresql://postgres@localhost:5432/quads", convert_unicode=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()


def init_db():

    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()
    from quads import models

    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)


def drop_all():

    Base.metadata.drop_all(bind=Engine)


def populate(app):
    admin_role = app.session.query(Role).filter(Role.name == "admin").first()
    user_role = app.session.query(Role).filter(Role.name == "user").first()
    commit = False
    if not admin_role:
        admin_role = Role(name="admin", description="Administrative role")
        app.session.add(admin_role)
        commit = True
    if not user_role:
        user_role = Role(name="user", description="Regular user role")
        app.session.add(user_role)
        commit = True

    user = user_datastore.get_user("grafuls@gmail.com")
    if not user:
        user_datastore.create_user(
            email="grafuls@gmail.com", password="password", roles=[admin_role]
        )
        commit = True

    if commit:
        app.session.commit()

    app.session.close()
