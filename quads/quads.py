import os

import mongoengine
import requests

from quads.config import Config
from quads.helpers import param_check


class Quads:
    """
    A python interface into the Quads API

    NOTE: Eventually the relationship of this class and API should be reversed.
        Considering both logic of API and the rest of quads is already written here in code
        there shouldn't be a need to have a http proxy for it.
    TODO: Separate heavy-lifting logic of API endpoints into it's own functions (or methods on this class)
        and have CLI and API depend on that
    """

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.API_URL
        self.session = requests.Session()

    @staticmethod
    def _param_check(*args, **kwargs):
        return param_check(*args, **kwargs)

    @staticmethod
    def connect_mongo():
        """
        Small wrapper for setting up mongo connection
        Mainly used by CLI, API/Flask has it's own way to connect (see flask-mongoengine)
        """
        ip = os.environ.get("MONGODB_IP", "127.0.0.1")
        mongoengine.connect("quads", ip)

    @staticmethod
    def _parse_and_check_quads(json_data):
        if json_data.status_code == 204:
            return "Resource properly removed"
        else:
            try:
                data = json_data.json()
            except ValueError:
                return []
            return data

    @staticmethod
    def _uri_constructor(_base_uri, _args):
        params = []
        if _args:
            for param in _args.items():
                params.append("=".join(param))
            params_uri = "&".join(params)
            _base_uri = "?".join([_base_uri, params_uri])
        return _base_uri

    def get(self, endpoint, **kwargs):
        uri = self._uri_constructor(endpoint, kwargs)
        _response = self.session.get(os.path.join(self.base_url, uri), verify=False)
        return self._parse_and_check_quads(_response)

    def post(self, endpoint, data):
        _response = self.session.post(os.path.join(self.base_url, endpoint), data, verify=False)
        return self._parse_and_check_quads(_response)

    def delete(self, endpoint, **kwargs):
        uri = self._uri_constructor(endpoint, kwargs)
        _response = self.session.delete(os.path.join(self.base_url, uri), verify=False)
        return self._parse_and_check_quads(_response)

    def get_hosts(self, **kwargs):
        uri = self._uri_constructor("host", kwargs)
        return self.get(uri)

    def get_clouds(self, **kwargs):
        uri = self._uri_constructor("cloud", kwargs)
        return self.get(uri)

    def get_cloud_hosts(self, cloud_name):
        hosts = []
        schedules = self.get_current_schedule(cloud=cloud_name)
        if "result" not in schedules:
            for schedule in schedules:
                host = self.get_hosts(id=schedule["host"]["$oid"])
                hosts.append(host)

        return hosts

    def get_schedules(self, **kwargs):
        uri = self._uri_constructor("schedule", kwargs)
        return self.get(uri)

    def get_current_schedule(self, **kwargs):
        uri = self._uri_constructor("current_schedule", kwargs)
        return self.get(uri)

    def remove_schedule(self, **kwargs):
        uri = self._uri_constructor("schedule", kwargs)
        return self.delete(uri)

    def remove_interface(self, **kwargs):
        uri = self._uri_constructor("interfaces", kwargs)
        return self.delete(uri)

    def insert_schedule(self, data):
        return self.post("schedule", data)

    def insert_cloud(self, data):
        return self.post("cloud", data)

    def get_available(self, **kwargs):
        uri = self._uri_constructor("available", kwargs)
        return self.get(uri)

    def get_summary(self, **kwargs):
        uri = self._uri_constructor("summary", kwargs)
        return self.get(uri)

    def get_interfaces(self, **kwargs):
        uri = self._uri_constructor("interfaces", kwargs)
        return self.get(uri)

    def get_version(self):
        uri = self._uri_constructor("version", None)
        return self.get(uri)
