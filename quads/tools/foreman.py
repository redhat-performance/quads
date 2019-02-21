#!/usr/bin/env python

import requests
import urllib3

urllib3.disable_warnings()


class Foreman(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get(self, endpoint):
        response = requests.get(
            self.url + endpoint,
            auth=(self.username, self.password),
            verify=False

        )
        response_json = response.json()
        hosts = {
            host["name"]: host
            for host in response_json["results"]
        }
        return hosts

    def get_idrac_host(self, host_name):
        _host_id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/interfaces/" % _host_id
        result = self.get(endpoint)
        for interface, details in result.items():
            if "mgmt" in interface:
                return interface
        return None

    def get_all_hosts(self):
        endpoint = "/hosts"
        return self.get(endpoint)

    def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return self.get(endpoint)

    def get_build_hosts(self, build=True):
        endpoint = "/hosts?search=params.build=%s" % str(build).lower()
        return self.get(endpoint)

    def get_parametrized(self, param, value):
        endpoint = "/hosts?search=%s=%s" % (param, value)
        return self.get(endpoint)

    def get_host_id(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get(endpoint)
        _id = result[host_name]["id"]
        return _id

    def get_host_param(self, host_name, param):
        _id = self.get_host_id(host_name)
        endpoint = "/hosts/%s/parameters?search=name=%s" % (_id, param)
        result = self.get(endpoint)
        value = result[host_name]["value"]
        return value

    def get_host_build_status(self, host_name):
        endpoint = "/hosts?search=name=%s" % host_name
        result = self.get(endpoint)
        build_status = result[host_name]["build_status"]
        return bool(build_status)
