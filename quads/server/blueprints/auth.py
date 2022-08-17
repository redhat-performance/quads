from flask import Blueprint, jsonify, request
from quads.server.app import user_datastore, db_session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def signup_user():
    data = request.get_json()
    user_datastore.create_user(email=data["email"], password=data["password"])
    db_session.commit()

    return jsonify({"message": "registered successfully"})
