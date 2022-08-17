#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, Blueprint, jsonify, Response
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

from quads.server.models import User, db, Role, Engine, Base

basic_auth = HTTPBasicAuth()
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    return True


def create_app(test_config=None) -> Flask:
    # create and configure the app
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.url_map.strict_slashes = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        flask_app.config.from_object("quads.server.config.DevelopmentConfig")
    else:
        # load the test config if passed in
        flask_app.config.from_mapping(test_config)

    db.init_app(flask_app)

    # populate()

    @flask_app.errorhandler(401)
    def error_401(ex) -> Response:
        return jsonify(
            {
                "status_code": 401,
                "error_description": "Unauthorized",
                "message": "You don't have right permissions for this resource",
            }
        )

    from quads.server.blueprints.assignments import assignment_bp
    from quads.server.blueprints.auth import auth_bp
    from quads.server.blueprints.clouds import cloud_bp
    from quads.server.blueprints.disks import disk_bp
    from quads.server.blueprints.hosts import host_bp
    from quads.server.blueprints.interfaces import interface_bp
    from quads.server.blueprints.memory import memory_bp
    from quads.server.blueprints.processors import processor_bp
    from quads.server.blueprints.schedules import schedule_bp
    from quads.server.blueprints.vlans import vlan_bp

    # Register blueprints
    api_prefix = f"/api/{flask_app.config.get('API_VERSION')}"
    api_bp = Blueprint("api", __name__, url_prefix=api_prefix)
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(assignment_bp, url_prefix="/assignments")
    api_bp.register_blueprint(host_bp, url_prefix="/hosts")
    api_bp.register_blueprint(cloud_bp, url_prefix="/clouds")
    api_bp.register_blueprint(interface_bp, url_prefix="/interfaces")
    api_bp.register_blueprint(schedule_bp, url_prefix="/schedules")
    api_bp.register_blueprint(vlan_bp, url_prefix="/vlans")
    api_bp.register_blueprint(disk_bp, url_prefix="/disks")
    api_bp.register_blueprint(processor_bp, url_prefix="/processors")
    api_bp.register_blueprint(memory_bp, url_prefix="/memory")
    flask_app.register_blueprint(api_bp)

    return flask_app


def init_db():

    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()

    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)
    db.init_app(app)


def populate():
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


if __name__ == "__main__":
    app = create_app()

    security = Security(app, user_datastore)
    migrate = Migrate(app, db)

    with app.app_context():
        init_db()
        populate()

    app.run()
