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
            host["name"]: {"ip": host["ip"], "mac": host["mac"]}
            for host in response_json["results"]
        }
        return hosts

    def get_all_hosts(self):
        endpoint = "/hosts"
        return self.get(endpoint)

    def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return self.get(endpoint)

    def get_parametrized(self, param, value):
        endpoint = "hosts?search=params.%s=%s" % (param, value)
        return self.get(endpoint)
