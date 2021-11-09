

def register_api_v2_endpoints(api: flask_restful.Api):
    from .moves import MovesEndpoint
    api.add_resource(MovesEndpoint, "/moves")
