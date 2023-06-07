import os
from typing import Optional, List

import requests
from requests import Response
from requests.auth import HTTPBasicAuth

from quads.config import Config
from quads.server.models import Host, Cloud, Schedule, Interface, Vlan, Assignment


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
        self.auth = HTTPBasicAuth(self.config.get("quads_api_username"), self.config.get("quads_api_password"))

    # Base functions
    def get(self, endpoint) -> Response:
        _response = self.session.get(
            os.path.join(self.base_url, endpoint), verify=False, auth=self.auth
        )
        return _response

    def post(self, endpoint, data) -> Response:
        _response = self.session.post(
            os.path.join(self.base_url, endpoint), json=data, verify=False, auth=self.auth
        )
        return _response

    def patch(self, endpoint, data) -> Response:
        _response = self.session.patch(
            os.path.join(self.base_url, endpoint), json=data, verify=False, auth=self.auth
        )
        return _response

    def delete(self, endpoint) -> Response:
        _response = self.session.delete(
            os.path.join(self.base_url, endpoint), verify=False, auth=self.auth
        )
        return _response

    # Hosts
    def get_hosts(self) -> List[Host]:
        response = self.get("hosts")
        hosts_json = response.json()
        hosts = []
        for host in hosts_json:
            host_obj = Host().from_dict(data=host)
            hosts.append(host_obj)
        return hosts

    def filter_hosts(self, data) -> List[Host]:
        response = self.post(os.path.join("hosts", "filter"), data)
        hosts = []
        for host in response.json():
            host_obj = Host().from_dict(data=host)
            hosts.append(host_obj)
        return hosts

    def get_host(self, hostname) -> Optional[Host]:
        host_obj = None
        response = self.get(os.path.join("hosts", hostname))
        obj_json = response.json()
        if obj_json:
            host_obj = Host().from_dict(data=obj_json)
        return host_obj

    def create_host(self, data) -> Host:
        response = self.post(os.path.join("hosts"), data)
        data = response.json()
        host_obj = Host().from_dict(data)
        return host_obj

    def update_host(self, hostname, data) -> Response:
        return self.patch(os.path.join("hosts", hostname), data)

    def remove_host(self, hostname) -> Response:
        return self.delete(os.path.join("hosts", hostname))

    def is_available(self, hostname, data) -> Response:
        return self.post(os.path.join("available", hostname), data)

    # Clouds
    def get_clouds(self) -> List[Cloud]:
        response = self.get("clouds")
        clouds = []
        for cloud in response.json():
            clouds.append(Cloud(**cloud))
        return clouds

    def filter_clouds(self, data) -> List[Cloud]:
        response = self.get("clouds", **data)
        clouds = []
        for cloud in response.json():
            clouds.append(Cloud(**cloud))
        return clouds

    def get_cloud(self, cloud_name) -> Optional[Cloud]:
        cloud_obj = None
        response = self.get(os.path.join("clouds", cloud_name))
        obj_json = response.json()
        if obj_json:
            cloud_obj = Cloud(**obj_json)
        return cloud_obj

    def insert_cloud(self, data) -> Response:
        return self.post("clouds", data)

    def remove_cloud(self, cloud_name) -> Response:
        return self.delete(os.path.join("clouds", cloud_name))

    # Schedules
    def get_schedules(self, data) -> List[Schedule]:
        response = self.get("schedules", **data)
        schedules = []
        for schedule in response.json():
            schedules.append(Schedule(**schedule))
        return schedules

    def get_current_schedules(self, data) -> List[Schedule]:
        response = self.post(os.path.join("schedules", "current"), data)
        schedules = []
        for schedule in response.json():
            schedules.append(Schedule(**schedule))
        return schedules

    def get_future_schedules(self, data) -> List[Schedule]:
        response = self.post(os.path.join("schedules", "future"), data)
        schedules = []
        for schedule in response.json():
            schedules.append(Schedule(**schedule))
        return schedules

    def update_schedule(self, schedule_id, data) -> Response:
        return self.post(os.path.join("schedules", schedule_id), data)

    def remove_schedule(self, schedule_id) -> Response:
        return self.delete(os.path.join("schedules", str(schedule_id)))

    def insert_schedule(self, data) -> Response:
        return self.post("schedules", data)

    # Available
    def get_available(self) -> List[Host]:
        response = self.get("available")
        hosts = []
        for host in response.json():
            hosts.append(Host(**host))
        return hosts

    # Available
    def get_moves(self) -> List:
        response = self.get("moves")
        hosts = []
        for host in response.json():
            hosts.append(Host(**host))
        return hosts

    def filter_available(self, data) -> List[Host]:
        response = self.get("available", **data)
        hosts = []
        for host in response.json():
            hosts.append(Host(**host))
        return hosts

    # Assignments
    def insert_assignment(self, data) -> Response:
        return self.post("assignments", data)

    def update_assignment(self, assignment_id, data) -> Response:
        return self.patch(os.path.join("assignments", str(assignment_id)), data)

    def get_active_cloud_assignment(self, cloud_name) -> Response:
        return self.get(os.path.join("assignments/active", cloud_name))

    def get_active_assignments(self) -> List[Assignment]:
        response = self.get("assignments/active")
        data = response.json()
        assignments = []
        for ass in data:
            ass_object = Assignment().from_dict(ass)
            assignments.append(ass_object)

        return assignments

    def get_assignment(self, **kwargs) -> Response:
        # TODO:fix this
        return self.get("assignments", **kwargs)

    # Interfaces
    def get_host_interface(self, hostname) -> List[Interface]:
        response = self.get(os.path.join("interfaces", hostname))
        data = response.json()
        interfaces = []
        for interface in data:
            interface_obj = Interface().from_dict(interface)
            interfaces.append(interface_obj)
        return interfaces

    def get_interfaces(self) -> Response:
        return self.get("interfaces")

    def update_interface(self, hostname, data) -> Response:
        return self.patch(os.path.join("interfaces", hostname), data)

    def remove_interface(self, interface_id) -> Response:
        return self.delete(os.path.join("interfaces", interface_id))

    def create_interface(self, hostname, data) -> Response:
        return self.post(os.path.join("interfaces", hostname), data)

    # Memory
    def create_memory(self, hostname, data) -> Response:
        return self.post(os.path.join("memory", hostname), data)

    def remove_memory(self, memory_id) -> Response:
        return self.delete(os.path.join("memory", memory_id))

    # Disks
    def create_disk(self, hostname, data) -> Response:
        return self.post(os.path.join("disk", hostname), data)

    def remove_disk(self, disk_id) -> Response:
        return self.delete(os.path.join("disk", disk_id))

    # Processor
    def create_processor(self, hostname, data) -> Response:
        return self.post(os.path.join("processor", hostname), data)

    def remove_processor(self, processor_id) -> Response:
        return self.delete(os.path.join("processor", processor_id))

    # Vlans
    def get_vlans(self) -> List[Vlan]:
        response = self.get("vlans")
        data = response.json()
        vlans = []
        for vlan in data:
            vlan_obj = Vlan().from_dict(vlan)
            vlans.append(vlan_obj)
        return vlans

    def get_summary(self) -> Response:
        return self.get("summary")

    def get_version(self) -> Response:
        return self.get("version")
