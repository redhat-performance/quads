from flask.blueprints import Blueprint

# typical blueprint and route usage
# main app.py then has to import this DocumentBP
# and call `app.register_blueprint(<DocumentBP>)`
# https://flask.palletsprojects.com/en/2.0.x/blueprints/


DocumentBP = Blueprint("DocumentBP", __name__)


@DocumentBP.route('/qinq')
def qinq_create_handler():
    pass
