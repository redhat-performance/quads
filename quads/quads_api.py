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

    # Base functions
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

    def patch(self, endpoint, data):
        _response = self.session.patch(
            os.path.join(self.base_url, endpoint), data, verify=False
        )
        return self.serialize(_response)

    def delete(self, endpoint, **kwargs):
        _response = self.session.delete(
            os.path.join(self.base_url, endpoint), verify=False
        )
        return self.serialize(_response)

    # Hosts
    def get_hosts(self):
        return self.get("hosts")

    def filter_hosts(self, data):
        return self.post(os.path.join("hosts", "filter"), data)

    def get_host(self, hostname):
        return self.get(os.path.join("hosts", hostname))

    def create_host(self, data):
        return self.post(os.path.join("hosts"), data)

    def update_host(self, hostname, data):
        return self.patch(os.path.join("hosts", hostname), data)

    def is_available(self, hostname, data):
        return self.post(os.path.join("available", hostname), data)

    # Clouds
    def get_clouds(self):
        return self.get("clouds")

    def filter_clouds(self, data):
        return self.get("clouds", **data)

    def get_cloud(self, cloud_name):
        return self.get(os.path.join("clouds", cloud_name))

    def insert_cloud(self, data):
        return self.post("clouds", data)

    # Schedules
    def get_schedules(self, data):
        return self.get("schedules", **data)

    def get_current_schedules(self, data):
        return self.post(os.path.join("schedules", "current"), data)

    def get_future_schedules(self, data):
        return self.post(os.path.join("schedules", "future"), data)

    def update_schedule(self, schedule_id, data):
        return self.post(os.path.join("schedules", schedule_id), data)

    def remove_schedule(self, schedule_id):
        return self.delete(os.path.join("schedules", schedule_id))

    def insert_schedule(self, data):
        return self.post("schedules", data)

    def get_available(self):
        return self.get("available")

    def filter_available(self, data):
        return self.get("available", **data)

    # Assignments
    def update_assignment(self, assignment_id, data):
        return self.patch(os.path.join("assignments", assignment_id), data)

    def get_active_cloud_assignment(self, cloud_name):
        return self.get(os.path.join("assignments/active", cloud_name))

    def get_assignment(self, data):
        # TODO:fix this
        return self.get("assignments", **data)

    # Interfaces
    def get_host_interface(self, hostname):
        return self.get(os.path.join("interfaces", hostname))

    def get_interfaces(self):
        return self.get("interfaces")

    def update_interface(self, hostname, data):
        return self.patch(os.path.join("interfaces", hostname), data)

    def remove_interface(self, interface_id):
        return self.delete(os.path.join("interfaces", interface_id))

    def create_interface(self, hostname, data):
        return self.post(os.path.join("interfaces", hostname), data)

    # Memory
    def create_memory(self, hostname, data):
        return self.post(os.path.join("memory", hostname), data)

    def remove_memory(self, memory_id):
        return self.delete(os.path.join("memory", memory_id))

    # Disks
    def create_disk(self, hostname, data):
        return self.post(os.path.join("disk", hostname), data)

    def remove_disk(self, disk_id):
        return self.delete(os.path.join("disk", disk_id))

    # Processor
    def create_processor(self, hostname, data):
        return self.post(os.path.join("processor", hostname), data)

    def remove_processor(self, processor_id):
        return self.delete(os.path.join("processor", processor_id))

    # Vlans
    def get_vlans(self):
        return self.get("vlans")

    def get_summary(self):
        return self.get("summary")

    def get_version(self):
        return self.get("version")
