#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_principal import (
    Principal,
    Permission,
    RoleNeed,
)
from quads.database import init_db, db_session
from quads.models import (
    Base,
    User,
    Role,
    Host,
    Cloud,
    Assignment,
    Notification,
    Vlan,
    Interface,
    Schedule,
)

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/quads"
auth = HTTPBasicAuth()

principals = Principal(app)
admin_permission = Permission(RoleNeed("admin"))


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

migrate = Migrate(app, db)

db.init_app(app)


def check_access(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)

            if role not in current_user.roles:
                return abort(401)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# @identity_loaded.connect_via(app)
# def on_identity_loaded(sender, identity):
#     identity.user = current_user
#
#     if hasattr(current_user, "email"):
#         identity.provides.add(UserNeed(current_user.email))
#
#     if hasattr(current_user, "role"):
#         for role in current_user.roles:
#             identity.provides.add(RoleNeed(role))


@app.before_first_request
def create_user():
    init_db()


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.route("/register", methods=["POST"])
def signup_user():
    data = request.get_json()
    user_datastore.create_user(email=data["email"], password=data["password"])
    db_session.commit()

    return jsonify({"message": "registered successfully"})


@app.route("/init/")
def init():
    admin_role = db_session.query(Role).filter(Role.name == "admin").first()
    user_role = db_session.query(Role).filter(Role.name == "user").first()
    commit = False
    if not admin_role:
        admin_role = Role(name="admin", description="Administrative role")
        db_session.add(admin_role)
        commit = True
    if not user_role:
        user_role = Role(name="user", description="Regular user role")
        db_session.add(user_role)
        commit = True

    user = user_datastore.get_user("grafuls@gmail.com")
    if not user:
        user_datastore.create_user(
            email="grafuls@gmail.com", password="password", roles=[admin_role]
        )
        commit = True

    if commit:
        db_session.commit()
    return jsonify({"message": "Initialization successful"})


@app.route("/hosts/")
def get_hosts():
    _hosts = db_session.query(Host).all()
    return jsonify([_host.as_dict() for _host in _hosts])


@app.route("/hosts/<hostname>/")
@check_access("admin")
def get_host(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify(_host.as_dict())


@app.route("/assignments/")
def get_assignments():
    _assignments = db - ession.query(Assignment).all()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@app.route("/assignments/<assignment_id>/")
@auth.login_required
def get_assignment(assignment_id):
    _assignment = (
        db_session.query(Assignment).filter(Assignment.id == assignment_id).first()
    )
    return jsonify(_assignment.as_dict())


@app.route("/interfaces/<hostname>")
def get_interfaces(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_interface.as_dict() for _interface in _host.interfaces])


@app.route("/disks/<hostname>")
def get_disks(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_disks.as_dict() for _disks in _host.disks])


@app.route("/memory/<hostname>")
def get_memory(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_memory.as_dict() for _memory in _host.memory])


@app.route("/processors/<hostname>")
def get_processors(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_processor.as_dict() for _processor in _host.processors])


@app.route("/clouds/")
def get_clouds():
    _clouds = db_session.query(Cloud).all()
    return jsonify([_cloud.as_dict() for _cloud in _clouds])


@app.route("/schedules/")
def get_schedules():
    _schedules = db_session.query(Schedule).all()
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@app.route("/schedules/<schedule_id>")
def get_schedule(schedule_id):
    _schedule = db_session.query(Schedule).filter(Schedule.id == schedule_id).first()
    return jsonify(_schedule.as_dict())


@app.route("/vlans/")
def get_vlans():
    _vlans = db_session.query(Vlan).all()
    return jsonify([_vlan.as_dict() for _vlan in _vlans])


@app.route("/clouds/<cloud>/")
def get_cloud(cloud):
    _cloud = db_session.query(Cloud).filter(Cloud.name == cloud).first()
    return jsonify(_cloud.as_dict())


@app.route("/hosts/", methods=["POST"])
def create_host():
    data = request.get_json()
    cloud_name = data.get("cloud")
    hostname = data.get("name")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _host = db_session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
        )

    if not host_type:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: host_type"}),
            400,
        )

    if default_cloud:
        _default_cloud = (
            db_session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Default Cloud not found: {default_cloud}",
                    }
                ),
                400,
            )
    else:
        return (
            jsonify(
                {"error": "Bad Request", "message": "Missing argument: default_cloud"}
            ),
            400,
        )

    _cloud = _default_cloud

    if cloud_name:
        _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )

    _host_obj = Host(
        name=hostname, host_type=host_type, cloud=_cloud, default_cloud=_default_cloud
    )
    db_session.add(_host_obj)
    db_session.commit()
    return jsonify(_host_obj.as_dict()), 201


@app.route("/assignments/", methods=["POST"])
def create_assignment():
    data = request.get_json()

    notification = Notification()
    _cloud = None
    _vlan = None
    cloud_name = data.get("cloud")
    vlan = data.get("vlan")
    description = data.get("description")
    owner = data.get("owner")
    ticket = data.get("ticket")
    qinq = data.get("qinq")
    wipe = data.get("wipe")
    cc_user = data.get("cc_user")

    if cloud_name:
        _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )

    if vlan:
        _vlan = db_session.query(Vlan).filter(Vlan.vlan_id == vlan).first()
        if not _vlan:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Vlan not found: {vlan}",
                    }
                ),
                400,
            )

    _assignment_obj = Assignment(
        description=description,
        owner=owner,
        ticket=ticket,
        qinq=qinq,
        wipe=wipe,
        ccuser=cc_user,
        vlan=_vlan,
        cloud=_cloud,
        notification=notification,
    )
    db_session.add(_assignment_obj)
    db_session.commit()
    return jsonify(_assignment_obj.as_dict()), 201


@app.route("/schedules/", methods=["POST"])
def create_schedule():
    data = request.get_json()

    hostname = data.get("hostname")
    cloud = data.get("cloud")
    _assignment = (
        db_session.query(Assignment)
        .filter(Assignment.cloud.name == cloud, Assignment.active == True)
        .first()
    )
    if not _assignment:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"No active assignment for cloud: {cloud}",
                }
            ),
            400,
        )

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: hostname"}),
            400,
        )

    _host = db_session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
        )

    start = data.get("start")
    end = data.get("end")

    _schedule_obj = Schedule(start=start, end=end, assignment=_assignment, host=_host)
    db_session.add(_schedule_obj)
    db_session.commit()

    return jsonify(_schedule_obj.as_dict()), 201


@app.route("/interfaces/<hostname>", methods=["POST"])
def create_interface(hostname):
    data = request.get_json()

    _host = db_session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
        )

    name = data.get("name")
    bios_id = data.get("bios_id")
    mac_address = data.get("mac_address")
    switch_ip = data.get("switch_ip")
    switch_port = data.get("switch_port")
    speed = data.get("speed")
    vendor = data.get("vendor")
    pxe_boot = data.get("pxe_boot")
    maintenance = data.get("maintenance")

    _interface_obj = Interface(
        name=name,
        bios_id=bios_id,
        mac_address=mac_address,
        switch_ip=switch_ip,
        switch_port=switch_port,
        speed=speed,
        vendor=vendor,
        pxe_boot=pxe_boot,
        maintenance=maintenance,
    )
    _host.interfaces.append(_interface_obj)
    db_session.add(_host)
    db_session.commit()
    return jsonify(_interface_obj.as_dict()), 201


@app.route("/clouds/", methods=["POST"])
def create_cloud():
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
    if _cloud:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Cloud {cloud_name} already exists",
                }
            ),
            400,
        )

    _cloud_obj = Cloud(name=cloud_name)
    db_session.add(_cloud_obj)
    db_session.commit()
    return jsonify(_cloud_obj.as_dict()), 201


@app.route("/hosts/", methods=["PUT"])
def update_host():
    data = request.get_json()
    cloud_name = data.get("cloud")
    hostname = data.get("name")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _host = db_session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify({"error": "Bad Request", "message": f"Host {hostname} not found"}),
            400,
        )

    if default_cloud:
        _default_cloud = (
            db_session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Default Cloud not found: {default_cloud}",
                    }
                ),
                400,
            )
        else:
            _host.default_cloud = _default_cloud
    else:
        return (
            jsonify(
                {"error": "Bad Request", "message": "Missing argument: default_cloud"}
            ),
            400,
        )

    if cloud_name:
        _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )
        else:
            _host.cloud = _cloud

    if host_type:
        _host.host_type = host_type

    db_session.commit()

    return jsonify(_host.as_dict()), 200


app.run()
