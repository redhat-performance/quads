import json
import os
import requests

from quads.config import Config


class MessengerDTO:
    def __init__(self, response):
        self.__dict__ = response.json()


class Generic:
    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj


class QuadsApi:
    """
    A python interface into the Quads API

    """

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.API_URL
        self.session = requests.Session()

    @staticmethod
    def serialize(_response):
        response_json = _response.json()
        response = json.loads(response_json, object_hook=Generic.from_dict)
        return response

    def get(self, endpoint, **kwargs):
        _response = self.session.get(
            os.path.join(self.base_url, endpoint), verify=False
        )
        return self.serialize(_response)

    def post(self, endpoint, data):
        _response = self.session.post(
            os.path.join(self.base_url, endpoint), data, verify=False
        )
        return self.serialize(_response)

    def delete(self, endpoint, **kwargs):
        _response = self.session.delete(
            os.path.join(self.base_url, endpoint), verify=False
        )
        return self.serialize(_response)

    def get_hosts(self):
        return self.get("hosts")

    def filter_hosts(self, data):
        return self.post(os.path.join("hosts", "filter"), data)

    def get_host(self, hostname):
        return self.get(os.path.join("hosts", hostname))

    def get_clouds(self):
        return self.get("clouds")

    def get_cloud(self, cloud_name):
        return self.get(os.path.join("clouds", cloud_name))

    def get_schedules(self, data):
        return self.get("schedules")

    def get_current_schedules(self, data):
        return self.post(os.path.join("schedules", "current"), data)

    def update_schedule(self, schedule_id, data):
        return self.post(os.path.join("schedules", schedule_id), data)

    def update_host(self, hostname, data):
        return self.post(os.path.join("hosts", hostname), data)

    def update_assignment(self, assignment_id, data):
        return self.post(os.path.join("assignments", assignment_id), data)

    def get_active_cloud_assignment(self, cloud_name):
        return self.get(os.path.join("assignments", cloud_name))

    def get_host_interface(self, hostname):
        return self.get(os.path.join("interfaces", hostname))

    def get_interfaces(self):
        return self.get("interfaces")

    def remove_schedule(self, schedule_id):
        return self.delete(os.path.join("schedules", schedule_id))

    def remove_interface(self, interface_id):
        return self.delete(os.path.join("interfaces", interface_id))

    def insert_schedule(self, data):
        return self.post("schedules", data)

    def insert_cloud(self, data):
        return self.post("clouds", data)

    def get_available(self, **kwargs):
        return self.get("available")

    def is_available(self, hostname, data):
        return self.post(os.path.join("available", hostname), data)

    def get_summary(self, **kwargs):
        return self.get("summary")

    def get_version(self):
        return self.get("version")
