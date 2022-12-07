import json

from flask import Blueprint, jsonify, request, make_response, Response

from quads.server.models import User, TokenBlackList, db, Role
from quads.server.app import basic_auth, user_datastore

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register/", methods=["POST"])
def register() -> Response:
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        response = {
            "status_code": 401,
            "status": "fail",
            "message": "Email or password cannot be left blank.",
        }
        return Response(response=json.dumps(response), status=401)

    user = user_datastore.get_user(email)
    role = db.session.query(Role).filter(Role.name == "user").first()
    if not user:
        try:
            user = user_datastore.create_user(
                email=email, password=password, roles=[role]
            )
            db.session.commit()
            auth_token = User.encode_auth_token(user.id)
            response_object = {
                "status": "success",
                "status_code": 200,
                "message": "Successfully registered",
                "auth_token": auth_token,
            }
            return jsonify(response_object)
        except Exception:
            response = {
                "status_code": 401,
                "status": "fail",
                "message": "An error occurred. Please try again.",
            }
            return Response(response=json.dumps(response), status=401)
    else:
        response = {
            "status_code": 401,
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return Response(response=json.dumps(response), status=401)


@auth_bp.route("/login/", methods=["POST"])
@basic_auth.login_required()
def login() -> Response:
    current_user = basic_auth.current_user()
    try:
        user = db.session.query(User).filter(User.email == current_user).first()
        auth_token = User.encode_auth_token(user.email)
        if auth_token:
            response_object = {
                "status_code": 201,
                "status": "success",
                "message": "Successful login",
                "auth_token": auth_token,
            }
            return jsonify(response_object)
        else:
            response = {
                "status_code": 401,
                "status": "fail",
                "message": "User does not exist.",
            }
            return Response(response=json.dumps(response), status=401)
    except Exception:
        response = {"status_code": 500, "status": "fail", "message": "Try again"}
        return Response(response=json.dumps(response), status=500)


@auth_bp.route("/logout/", methods=["POST"])
def logout() -> Response:
    # get auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        user = user_datastore.get_user(resp)
        if user:
            token_blacklist = TokenBlackList(token=auth_token)
            try:
                db.session.add(token_blacklist)
                db.session.commit()
                response_object = {
                    "status": "success",
                    "message": "Successfully logged out.",
                }
                return jsonify(response_object)
            except Exception as e:
                response = {"status": "fail", "message": e}
                return Response(response=json.dumps(response), status=400)
        else:
            response = {"status": "fail", "message": resp}
            return Response(response=json.dumps(response), status=401)
    else:
        response = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return Response(response=json.dumps(response), status=403)
