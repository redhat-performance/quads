# this class will inherit from hardware_service.py and overwrite all of its methods
# with hil-specific behaviors - mostly through api calls to the HIL server

from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
import requests
import logging
import json
from subprocess import call
from subprocess import check_call

from hardware_services.inventory_service import InventoryService

# added for EC528 HIL-QUADS integration project
hil_url = 'http://127.0.0.1:5000'

class HilInventoryDriver(InventoryService):


    def update_cloud(self, quadsinstance, **kwargs):
        quadsinstance.quads_rest_call('PUT', hil_url, '/project/' + kwargs['cloudresource'])
        quadsinstance.quads_rest_call('PUT', hil_url, '/network/' + kwargs['cloudresource'], json.dumps({"owner": kwargs['cloudresource'], "access": kwargs['cloudresource'], "net_id": ""}))


    def update_host(self, quadsinstance, **kwargs):
        quadsinstance.quads_rest_call('POST', hil_url, '/project/' + kwargs['hostcloud'] + '/connect_node', json.dumps({'node': kwargs['hostresource']}))
        node_info = quadsinstance.quads_rest_call('GET', hil_url, '/node/' + kwargs['hostresource'])
        node = node_info.json()
        for nic in node['nics']:        # a node in quads will only have one nic per network
            quadsinstance.quads_rest_call('POST', hil_url, '/node/' + kwargs['hostresource'] + '/nic/' + nic['label'] + '/connect_network', json.dumps({'network': kwargs['hostcloud']}))



    def remove_cloud(self, quadsinstance, **kwargs):
        targetProject = kwargs['rmcloud']
        quadsinstance.quads_rest_call("DELETE", hil_url, '/network/'+ targetProject)
        quadsinstance.quads_rest_call("DELETE", hil_url, '/project/'+ targetProject)


    def remove_host(self,quadsinstance, **kwargs):
        # first detach host from network
        node_info = quadsinstance.quads_rest_call('GET', hil_url, '/node/' + kwargs['rmhost'])
        node = node_info.json()
        for nic in node['nics']:        # a node in quads will only have one nic per network
            quadsinstance.quads_rest_call('POST', hil_url, '/node/' + kwargs['rmhost'] + '/nic/' + nic['label'] + '/detach_network', json.dumps({'network': node['project']}))


    def list_clouds(self, quadsinstance):
        projects = quadsinstance.quads_rest_call("GET", hil_url, '/projects')
        print projects.text


    def list_hosts(self, quadsinstance):
        hosts = quadsinstance.quads_rest_call("GET", hil_url, '/nodes/all')
        #hosts_yml = yaml.dump(json.loads(hosts.text), default_flow_style=False)
        print hosts.text



