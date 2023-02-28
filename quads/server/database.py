from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from quads.server.models import Base, Engine, db, Role

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def init_db():

    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()

    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)


def drop_all():
    Base.metadata.drop_all(bind=Engine)


def populate(user_datastore):
    admin_role = db.session.query(Role).filter(Role.name == "admin").first()
    user_role = db.session.query(Role).filter(Role.name == "user").first()
    commit = False
    if not admin_role:
        admin_role = Role(name="admin", description="Administrative role")
        db.session.add(admin_role)
        commit = True
    if not user_role:
        user_role = Role(name="user", description="Regular user role")
        db.session.add(user_role)
        commit = True

    regular_user = "gonza@redhat.com"
    admin_user = "grafuls@redhat.com"

    user = user_datastore.get_user(admin_user)
    if not user:
        user_datastore.create_user(
            email=admin_user, password="password", roles=[admin_role]
        )
        commit = True

    user = user_datastore.get_user(regular_user)
    if not user:
        user_datastore.create_user(
            email=regular_user, password="password", roles=[user_role]
        )
        commit = True

    if commit:
        db.session.commit()
