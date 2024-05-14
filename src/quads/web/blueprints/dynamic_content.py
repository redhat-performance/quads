import os

from flask import Blueprint, abort, render_template
from quads.config import Config

WEB_CONTENT_PATH = Config.get("web_content_path")
EXCLUDE_DIRS = Config.get("web_exclude_dirs")

STATIC_DIR = os.path.join(WEB_CONTENT_PATH, "static")
dynamic_content_bp = Blueprint(
    "content",
    __name__,
    template_folder=WEB_CONTENT_PATH,
    static_folder=STATIC_DIR,
    static_url_path="/content",
)


@dynamic_content_bp.route("/<page>")
def dynamic_content(page):
    file_paths = get_file_paths()
    for file in file_paths:
        if page in file:
            return render_template(file)
    return abort(404)


@dynamic_content_bp.route("/<directory>/<page>")
def dynamic_content_sub(directory, page):
    file_paths = get_file_paths()
    for file in file_paths:
        if page in file:
            return render_template(os.path.join(directory, file))
    return abort(404)


def get_file_paths(web_path: str = WEB_CONTENT_PATH):
    file_paths = []
    for root, dirs, files in os.walk(web_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            file_paths.append(file)
    return file_paths
