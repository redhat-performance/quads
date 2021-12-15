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
        _response = self.session.post(
            os.path.join(self.base_url, endpoint), data, verify=False
        )
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
