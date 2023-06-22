from werkzeug.test import TestResponse


def unwrap_json(response: TestResponse) -> TestResponse:
    """
    Unwrap a response from the API, which always returns a JSON data, but
    on failure it's wrapped in Response and to use the included json method
    we need to change the content_type from `text/html` to `application/json`.
    """
    if response.content_type != "application/json":
        response.content_type = "application/json"
    return response
