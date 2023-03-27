#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, Blueprint, jsonify, Response
from flask_security import SQLAlchemySessionUserDatastore

from quads.server.database import populate, drop_all
from quads.server.database import init_db as db_init
from quads.server.extensions import basic_auth, security, login_manager
from quads.server.models import User, db, Role, migrate


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

    register_extensions(flask_app)
    register_blueprints(flask_app)

    @flask_app.errorhandler(401)
    def error_401(ex) -> Response:
        return jsonify(
            {
                "status_code": 401,
                "error_description": "Unauthorized",
                "message": "You don't have right permissions for this resource",
            }
        )

    @flask_app.cli.command("init-db")
    def init_db():
        """Creates the db tables."""
        with flask_app.app_context():
            db_init(flask_app.config)
            populate(user_datastore)

    @flask_app.cli.command("drop-db")
    def drop_db():
        """Drops the db tables."""
        with flask_app.app_context():
            drop_all(flask_app.config)

    return flask_app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    security.init_app(app, user_datastore)


def register_blueprints(app):
    from quads.server.blueprints.moves import moves_bp
    from quads.server.blueprints.assignments import assignment_bp
    from quads.server.blueprints.auth import auth_bp
    from quads.server.blueprints.available import available_bp
    from quads.server.blueprints.clouds import cloud_bp
    from quads.server.blueprints.disks import disk_bp
    from quads.server.blueprints.hosts import host_bp
    from quads.server.blueprints.interfaces import interface_bp
    from quads.server.blueprints.memory import memory_bp
    from quads.server.blueprints.processors import processor_bp
    from quads.server.blueprints.schedules import schedule_bp
    from quads.server.blueprints.vlans import vlan_bp

    # Register blueprints
    api_prefix = f"/api/{app.config.get('API_VERSION')}"
    api_bp = Blueprint("api", __name__, url_prefix=api_prefix)
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(available_bp, url_prefix="/available")
    api_bp.register_blueprint(assignment_bp, url_prefix="/assignments")
    api_bp.register_blueprint(host_bp, url_prefix="/hosts")
    api_bp.register_blueprint(cloud_bp, url_prefix="/clouds")
    api_bp.register_blueprint(interface_bp, url_prefix="/interfaces")
    api_bp.register_blueprint(schedule_bp, url_prefix="/schedules")
    api_bp.register_blueprint(vlan_bp, url_prefix="/vlans")
    api_bp.register_blueprint(disk_bp, url_prefix="/disks")
    api_bp.register_blueprint(processor_bp, url_prefix="/processors")
    api_bp.register_blueprint(memory_bp, url_prefix="/memory")
    api_bp.register_blueprint(moves_bp, url_prefix="/moves")
    app.register_blueprint(api_bp)
