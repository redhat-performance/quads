from functools import wraps

from flask import request, abort

from quads.server.models import User, db, Role


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
                username = User.decode_auth_token(token)
                current_user = (
                    db.session.query(User).filter(User.email == username).first()
                )
                if current_user is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized",
                    }, 401
                if not current_user.active:
                    abort(403)
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                }, 500

            role_obj = db.session.query(Role).filter(Role.name == role).first()
            if role_obj not in current_user.roles:
                return abort(401)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
