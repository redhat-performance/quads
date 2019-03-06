#!/usr/bin/env python
import logging
import requests
import urllib3
from requests import RequestException

urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Foreman(object):
    def __init__(self, url, username, password):
        logger.debug(":Initializing Foreman object:")
        self.url = url
        self.username = username
        self.password = password

    def get(self, endpoint):
        logger.debug("GET: %s" % endpoint)
        try:
            response = requests.get(
                self.url + endpoint,
                auth=(self.username, self.password),
                verify=False

            )
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
        return response.json()

    def get_host_dict(self, endpoint):
        response_json = self.get(endpoint)
        hosts = {
            host["name"]: host
            for host in response_json["results"]
        }
        return hosts

    def put_host_parameter(self, host_name, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s" % _host_id
        data = {
            'host': {
                'host_parameters_attributes': [
                    {"name": name},
                    {"value": value}
                ]
            }
        }
        try:
            response = requests.put(self.url + endpoint, data, verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 204]:
            return True
        return False

    def put_parameter(self, host_name, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s" % _host_id
        data = {
            'host': {name: value}
        }
        try:
            response = requests.put(self.url + endpoint, data, verify=False)
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong with your request.")
            return False
        if response.status_code in [200, 204]:
            return True
        return False

    def put_parameter_by_name(self, host, name, value):
        logger.debug("PUT param: {%s:%s}" % (name, value))
        param_id = None
        if name == "media":
            put_name = "medium"
        else:
            put_name = name[:-1]
        endpoint = "/%s" % name
        result = self.get(endpoint)
        for item in result["results"]:
            if "name" in item and item["name"] == value:
                param_id = item["id"]
        if param_id:
            self.put_parameter(host, "%s_id" % put_name, param_id)
            self.put_parameter(host, "%s_name" % put_name, value)
            return True
        return False

    def get_idrac_host(self, host_name):
        logger.debug("GET idrac: %s" % host_name)
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = self.get_host_dict(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return interface
        return None

    def get_all_hosts(self):
        endpoint = "/hosts"
        return self.get_host_dict(endpoint)

    def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return self.get_host_dict(endpoint)

    def get_build_hosts(self, build=True):
        endpoint = "/hosts?search=params.build=%s" % str(build).lower()
        return self.get_host_dict(endpoint)

    def get_parametrized(self, param, value):
        endpoint = "/hosts?search=%s=%s" % (param, value)
        return self.get_host_dict(endpoint)

    def get_host_id(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get_host_dict(endpoint)
        _id = result[host_name]["id"]
        return _id

    def get_host_param(self, host_name, param):
        _id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (_id, param)
        result = self.get_host_dict(endpoint)
        value = result[host_name]["value"]
        return value

    def get_host_build_status(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get_host_dict(endpoint)
        build_status = result[host_name]["build_status"]
        return bool(build_status)

    def get_host_extraneous_interfaces(self, host_id):
        endpoint = "/hosts/%s/interfaces" % host_id
        response_json = self.get(endpoint)
        extraneous_interfaces = [i for i in response_json["results"] if i["identifier"] != "mgmt" and not i["primary"]]
        return extraneous_interfaces

    def remove_extraneous_interfaces(self, host):
        _host_id = self.get_host_id(host)
        success = True
        extraneous_interfaces = self.get_host_extraneous_interfaces(_host_id)
        for interface in extraneous_interfaces:
            endpoint = "/hosts/%s/interfaces/%s" % (_host_id, interface["id"])
            try:
                response = requests.delete(endpoint)
            except RequestException as ex:
                logger.debug(ex)
                logger.error("There was something wrong with your request.")
                success = False
                continue
            if response.status_code != 200:
                success = False
        return success
