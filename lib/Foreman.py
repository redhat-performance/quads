#!/usr/bin/env python

import requests


class Foreman(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_hosts(self, endpoint):
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
        return self.get_hosts(endpoint)

    def get_broken_hosts(self):
        endpoint = "/hosts?search=params.broken_state=true"
        return self.get_hosts(endpoint)
