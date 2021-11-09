import json

from flask import Flask
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from quads.server.api.web import WebBP

app = Flask(__name__)


# app should also setup mongoengine connection somewhere here
# so that when other views start accessing methods, mongoengine is already connected
# either call quads.connect_mongo() or use flask_mongoengine


class JsonApi(Api):
    # This feels like hack, but it's the only way I found how to make HTTP errors return as json

    def handle_error(self, e: Exception):
        """Return our JSON instead of HTML for HTTP errors."""
        # print("wtf:", repr(e))
        if isinstance(e, HTTPException):
            response = e.get_response()
            response.content_type = "application/json"

            data = json.dumps({"result": e.description})

            response.data = data
            return response

        return super(JsonApi, self).handle_error(e)


api = JsonApi(app)

# url_prefix = /, eg. use this blueprint as index
# other blueprints would for example have
# url_prefix = "/api", and you can chain BPs so, "/api/auth", "/api/model/host", etc

app.register_blueprint(WebBP, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=False)
