#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from flask import abort, request
from flask_httpauth import HTTPBasicAuth
from flask_security import Security, SQLAlchemySessionUserDatastore
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
basic_auth = HTTPBasicAuth()

principals = Principal(app)
admin_permission = Permission(RoleNeed("admin"))


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(app.session, User, Role)
security = Security(app, user_datastore)

migrate = Migrate(app, app.session)


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
                data = User.decode_auth_token(token, app)
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


@basic_auth.verify_password
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
