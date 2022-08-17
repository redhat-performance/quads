from functools import wraps

from flask import request, abort

from quads.server.models import User, user_datastore


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
