from sqlalchemy_utils import database_exists, create_database
from quads.server.models import Base, Role, User, engine_from_config, db


def init_db(config=None):
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()
    if config:
        Engine = engine_from_config(config)
    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)


def drop_all(config=None):
    if config:
        Engine = engine_from_config(config)
    Base.metadata.drop_all(bind=Engine)


def populate(user_datastore):
    admin_role_name = "admin"
    admin_role_description = "Administrative role"

    user_role_name = "user"
    user_role_description = "Regular user role"

    admin_role = create_role(admin_role_name, admin_role_description)
    user_role = create_role(user_role_name, user_role_description)

    regular_user = "gonza@redhat.com"
    admin_user = "grafuls@redhat.com"

    admin_user_added = create_user(user_datastore, admin_user, "password", [admin_role])
    regular_user_added = create_user(user_datastore, regular_user, "password", [user_role])

    if admin_role or user_role or admin_user_added or regular_user_added:
        db.session.commit()


def create_user(user_datastore, email, password, roles):
    user_entry = db.session.query(User).filter(User.email == email).first()
    if not user_entry:
        user_datastore.create_user(email=email, password=password, roles=roles)
        return True
    return False


def create_role(name, description):
    role_entry = db.session.query(Role).filter(Role.name == name).first()
    if not role_entry:
        role = Role(name=name, description=description)
        db.session.add(role)
        return role
    return role_entry
