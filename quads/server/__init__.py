from flask import Flask, Blueprint
from sqlalchemy.orm import scoped_session

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
from quads.server.extensions import database
from quads.server.extensions.database import SessionLocal, populate


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

    app.session = scoped_session(SessionLocal)
    populate(app)

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
