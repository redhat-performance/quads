import os

from flask import Blueprint, render_template, abort
from quads.config import Config

WEB_CONTENT_PATH = Config.get("web_content_path")
EXCLUDE_DIRS = Config.get("web_exclude_dirs")

dynamic_content_bp = Blueprint("content", __name__, template_folder=WEB_CONTENT_PATH)


@dynamic_content_bp.route("/<page>")
def dynamic_content(page):
    file_paths = get_file_paths()
    for file in file_paths:
        if page in file:
            return render_template(file)
    return abort(404)


def get_file_paths(web_path: str = WEB_CONTENT_PATH):
    file_paths = []
    for root, dirs, files in os.walk(web_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            file_paths.append(file)
    return file_paths
