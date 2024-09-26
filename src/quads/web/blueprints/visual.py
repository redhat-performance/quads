import os

from flask import Blueprint, abort, render_template

from quads.web.blueprints.common import WEB_CONTENT_PATH, get_file_paths

TEMPLATE_DIR = os.path.join(WEB_CONTENT_PATH, "visual")
visual_bp = Blueprint(
    "visual",
    __name__,
    template_folder=TEMPLATE_DIR,
)


@visual_bp.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e), 500


@visual_bp.route("/<when>")
def visuals(when):
    path = os.path.join(WEB_CONTENT_PATH, "visual")
    file_paths = get_file_paths(path)
    for file in file_paths:
        if when in file:
            return render_template(file)
    return abort(404)
