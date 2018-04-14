"""HIL Client library.

This is the main client library module that users of this library will
be interested in; importing other modules directly is typically unnecessary.
"""
from hil.client.node import Node
from hil.client.project import Project
from hil.client.switch import Switch
from hil.client.switch import Port
from hil.client.network import Network
from hil.client.user import User
from hil.client.extensions import Extensions
import abc
import requests

from collections import namedtuple


class HTTPClient(object):
    """An HTTP client.

    Makes HTTP requests on behalf of the HIL CLI. Responsible for adding
    authentication information to the request.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request(self, method, url, data=None, params=None):
        """Make an HTTP request

        Makes an HTTP request on URL `url` with method `method`, request body
        `data`(if supplied) and query parameter `params`(if supplied). May add
        authentication or other backend-specific information to the request.

        Parameters
        ----------

        method : str
            The HTTP method to use, e.g. 'GET', 'PUT', 'POST'...
        url : str
            The URL to act on
        data : str, optional
            The body of the request
        params : dictionary, optional
            The query parameter, e.g. {'key1': 'val1', 'key2': 'val2'},
            dictionary key can't be `None`

        Returns
        -------

        HTTPResponse
            The HTTP response
        """


class HTTPResponse(namedtuple('HTTPResponse', ['status_code',
                                               'headers',
                                               'content'])):
    """An http response.

    Attributes
    ----------

    status_code : int
        The http status code
    headers : dict
        http headers
    content : str
        The body of the response
    """


class RequestsHTTPClient(requests.Session, HTTPClient):
    """An HTTPClient which uses the requests library.

    This is a thin wrapper around `requests.Session`; all it does is
    convert the response to an `HTTPResponse`.

    The requests library's Response object actually satisfies the
    needed interface by itself, but by wrapping it we decrease the
    odds of accidentally depending on requests-specific functionality.
    """

    # disable a pylint warning about arguments that don't match the
    # superclass's; we just pass these straight through to the super
    # class's method, so *args, **kwargs let's us ignore what they
    # are entirely.
    #
    # pylint: disable=arguments-differ
    def request(self, *args, **kwargs):
        resp = requests.Session.request(self, *args, **kwargs)
        return HTTPResponse(status_code=resp.status_code,
                            headers=resp.headers,
                            content=resp.content)


class KeystoneHTTPClient(HTTPClient):
    """An HTTPClient which authenticates with Keystone.

    This uses an instance of python-keystoneclient's Session class
    to do its work.
    """

    def __init__(self, session):
        """Create a KeystoneHTTPClient

        Parameters
        ----------

        session : keystoneauth1.Session
            A keystone session to make the requests with
        """
        self.session = session

    def request(self, method, url, data=None, params=None):
        """Make an HTTP request using keystone for authentication.

        Smooths over the differences between python-keystoneclient's
        request method that specified by HTTPClient
        """
        # We have to import this here, since we can't assume the library
        # is available from global scope.
        from keystoneauth1.exceptions.http import HttpError

        try:
            # The order of these parameters is different that what
            # we expect, but the names are the same:
            resp = self.session.request(method=method,
                                        url=url,
                                        data=data,
                                        params=params)

        except HttpError as e:
            resp = e.response
        return HTTPResponse(status_code=resp.status_code,
                            headers=resp.headers,
                            content=resp.content)


class Client(object):
    """A HIL API client."""

    def __init__(self, endpoint, httpClient):
        self.httpClient = httpClient
        self.endpoint = endpoint
        self.node = Node(self.endpoint, self.httpClient)
        self.project = Project(self.endpoint, self.httpClient)
        self.switch = Switch(self.endpoint, self.httpClient)
        self.port = Port(self.endpoint, self.httpClient)
        self.network = Network(self.endpoint, self.httpClient)
        self.user = User(self.endpoint, self.httpClient)
        self.extensions = Extensions(self.endpoint, self.httpClient)
