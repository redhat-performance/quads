from flask import Blueprint, Response, jsonify

from quads.config import Config

version_bp = Blueprint("version", __name__)


@version_bp.route("/")
def get_version() -> Response:
    response = {
        "result": f"QUADS version {Config.QUADSVERSION} {Config.QUADSCODENAME}"
    }
    return jsonify(response)
