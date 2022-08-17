from flask import Blueprint, jsonify, request, make_response

from quads.server.models import User, TokenBlackList, db, user_datastore

# from quads.server.app import basic_auth

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = user_datastore.get_user(email=data.get("email"))

    if not user:
        try:
            user = user_datastore.create_user(
                email=data["email"], password=data["password"]
            )
            db.session.commit()
            auth_token = User.encode_auth_token(user.id)
            response_object = {
                "status": "success",
                "message": "Succesfully registered",
                "auth_token": auth_token,
            }
            return make_response(jsonify(response_object)), 201
        except Exception as ex:
            response_object = {
                "status": "fail",
                "message": "An error occurred. Please try again.",
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return make_response(jsonify(response_object)), 202


@auth_bp.route("/login", methods=["POST"])
# @basic_auth.login_required()
def login():
    data = request.get_json()
    try:
        user = user_datastore.get_user(email=data.get("email"))
        if user and user.verify_password(data.get("password")):
            auth_token = User.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successful login",
                    "auth_token": auth_token,
                }
                return make_response(jsonify(response_object)), 201
        else:
            response_object = {"status": "fail", "message": "User does not exist."}
            return make_response(jsonify(response_object)), 404
    except Exception as ex:
        response_object = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response_object)), 500


@auth_bp.route("/logout")
def logout():
    # get auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            token_blacklist = TokenBlackList(token=auth_token)
            try:
                db.session.add(token_blacklist)
                db.session.commit()
                response_object = {
                    "status": "success",
                    "message": "Successfully logged out.",
                }
                return make_response(jsonify(response_object)), 200
            except Exception as e:
                response_object = {"status": "fail", "message": e}
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {"status": "fail", "message": resp}
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 403
