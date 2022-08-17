#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from flask import jsonify, abort
from flask_httpauth import HTTPBasicAuth
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from flask_migrate import Migrate
from flask_principal import (
    Principal,
    Permission,
    RoleNeed,
)
from quads.models import (
    User,
    Role,
)
from quads.server import create_app


app = create_app()
auth = HTTPBasicAuth()

principals = Principal(app)
admin_permission = Permission(RoleNeed("admin"))


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(app.session, User, Role)
security = Security(app, user_datastore)

migrate = Migrate(app, db)


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


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


if __name__ == "__main__":
    app.run()
