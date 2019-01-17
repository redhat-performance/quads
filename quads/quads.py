import os
import requests


class Api(object):
    """
    A python interface into the Quads API
    """

    def __init__(self, base_url):
        """
        Initialize a quads object.
        """
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def _parse_and_check_quads(json_data):
        try:
            data = json_data.json()
        except ValueError:
            return None
        return data

    @staticmethod
    def _uri_constructor(base_uri, args):
        params = []
        if args:
            for param in args.items():
                params.append("=".join(param))
            params_uri = "&".join(params)
            base_uri = "?".join([base_uri, params_uri])
        return base_uri

    def get(self, endpoint):
        _response = self.session.get(os.path.join(self.base_url, endpoint))
        return self._parse_and_check_quads(_response)

    def get_hosts(self, **kwargs):
        uri = self._uri_constructor("host", kwargs)
        return self.get(uri)

    def get_cloud(self, **kwargs):
        uri = self._uri_constructor("cloud", kwargs)
        return self.get(uri)

    def get_schedule(self, **kwargs):
        uri = self._uri_constructor("schedule", kwargs)
        return self.get(uri)

    def get_current_schedule(self, **kwargs):
        uri = self._uri_constructor("current_schedule", kwargs)
        return self.get(uri)
