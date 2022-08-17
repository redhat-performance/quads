#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from flask import Flask, Blueprint, abort, request
from flask_security import Security
from flask_httpauth import HTTPBasicAuth

from quads.server.models import User, db, user_datastore


def check_access(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401
            try:
                data = User.decode_auth_token(token)
                current_user = user_datastore.get_user(data["sub"])
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized",
                    }, 401
                if not current_user["active"]:
                    abort(403)
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                }, 500

            if role not in current_user.roles:
                return abort(401)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        app.config.from_object("config.DevelopmentConfig")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    # populate()
    security = Security(app, user_datastore)

    basic_auth = HTTPBasicAuth()

    @basic_auth.verify_password
    def verify_password(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            return False
        return True

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
    api_prefix = f"/api/{app.config.get('API_VERSION')}"
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
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    # Setup Flask-Security

    app.run()
