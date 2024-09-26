import os

from flask import Blueprint, abort, render_template

from quads.web.blueprints.common import WEB_CONTENT_PATH, get_file_paths

TEMPLATE_DIR = os.path.join(WEB_CONTENT_PATH, "instack")
instack_bp = Blueprint(
    "instack",
    __name__,
    template_folder=TEMPLATE_DIR,
)


@instack_bp.route("/instack/<cloud>")
def instack(cloud):
    path = os.path.join(WEB_CONTENT_PATH, "instack")
    file_paths = get_file_paths(path)
    for file in file_paths:
        if cloud in file:
            return render_template(file)
    return abort(404)
