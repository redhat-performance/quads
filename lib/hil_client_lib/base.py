""" This module implements the HIL client library. """

from urlparse import urljoin
import json
import re
from hil.errors import BadArgumentError
import inspect


class FailedAPICallException(Exception):
    """An exception indicating that the server returned an error.

    Attributes:

        error_type (str): the type of the error. This will be the name of
            one of the subclasses of APIError in hil.errors.
        message (str): a human readble description of the error.
    """

    def __init__(self, error_type, message):
        Exception.__init__(self, message)
        self.error_type = error_type


class ClientBase(object):
    """Main class which contains all the methods to

    -- ensure input complies to API requisites
    -- generates correct format for server API on behalf of the client
    -- parses output from received from the server.
    In case of errors recieved from server, it will generate appropriate
    appropriate message.
    """

    def __init__(self, endpoint, httpClient):
        """ Initialize an instance of the library with following parameters.

       endpoint: stands for the http endpoint eg. endpoint=http://127.0.0.1
       sess: depending on the authentication backend (db vs keystone) the
       parameters required to make up the session vary.
       user: username as which you wish to connect to HIL
       Currently all this information is fetched from the user's environment.
        """
        self.endpoint = endpoint
        self.httpClient = httpClient

    def object_url(self, *args):
        """Generate URL from combining endpoint and args as relative URL"""
        rel = "/".join(args)
        url = urljoin(self.endpoint, rel)
        return url

    def check_response(self, response):
        """
        Check the response from an API call, and do any needed error handling

        Returns the body of the response as (parsed) JSON, or None if there
        was no body. Raises a FailedAPICallException on any non 2xx status.
        """
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content)
            except ValueError:  # No JSON request body; typical
                                # For methods PUT, POST, DELETE
                return
        try:
            e = json.loads(response.content)
            raise FailedAPICallException(
                error_type=e['type'],
                message=e['msg'],
            )
        # Catching responses that do not return JSON
        except ValueError:
            return response.content


def _find_reserved(string, slashes_ok=False):
    """Returns a list of illegal characters in a string"""
    p = r"[^A-Za-z0-9 /$_.+!*'(),-]"
    result = re.findall(p, string)
    if not slashes_ok and '/' in string:
        result.append('/')
    # return one of each illegal character in string
    return list(set(result))


def check_reserved(obj_type, obj_string, slashes_ok=False):
    """Check for illegal characters and report of their existence"""
    bad_chars = _find_reserved(obj_string, slashes_ok)
    if bool(bad_chars):
        error = obj_type + " may not contain: " + str(bad_chars)
        raise BadArgumentError(error)


def check_reserved_chars(*outer_args, **outer_kwargs):
    """Wraps Client lib functions to check for illegal characters
    and dynamically report the error by the offending argument(s)"""
    def wrapper(f):
        """Auxiliary wrapper for check_reserved_chars"""

        argspec = inspect.getargspec(f)

        def reserved_wrap(*args, **kwargs):
            """Wrapper that is passed the arguments of the wrapped function"""
            dont_check = outer_kwargs.get('dont_check', [])
            slashes_ok = outer_kwargs.get('slashes_ok', [])
            # Looping begins at 1 to skip `self` argument
            for argname, argval in zip(argspec.args[1:], args[1:]):
                if argname not in dont_check:
                    check_reserved(argname, argval,
                                   slashes_ok=argname in slashes_ok)
            return f(*args, **kwargs)
        return reserved_wrap
    return wrapper
