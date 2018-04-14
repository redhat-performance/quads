#!/usr/bin/env python
"""This module sets up a HIL client"""

import sys
import os
import requests
import yaml

from quads_config import quads_load_config

#Parsing the quads config file
#quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
quads_config_file = os.path.dirname(os.path.abspath(__file__)) + "/../conf/quads.yml"
quads_config = quads_load_config(quads_config_file)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/hil_client_lib/")

from client import Client, RequestsHTTPClient, KeystoneHTTPClient


def setup_http_client():
    """Set `http_client` to a valid instance of `HTTPClient`

    and pass it as parameter to initialize the client library of HIL.

    Sets http_client to an object which makes HTTP requests with
    authentication. It chooses an authentication backend as follows:

    1. If the variables 'allocator_url', 'allocator_username', and 
       'allocator_password' are defined in the `quads.yml`,
       it will use HTTP basic auth, with the corresponding
       user name and password.
    2. If the `python-keystoneclient` library is installed, and then 
        make sure following keys are defined in `quads.yml` with appropriate
        values:

           * OS_AUTH_URL
           * OS_USERNAME
           * OS_PASSWORD
           * OS_PROJECT_NAME

       If these keys are available then Keystone will be used 
       to initialize the HIL library.
    """
    
    # First try basic auth:
    ep = quads_config['allocator_url']

    if ep is None:
        sys.exit("Error: Allocator_url not set \n")

    basic_username = quads_config['allocator_username']
    basic_password = quads_config['allocator_password']
    if basic_username is not None and basic_password is not None:
        # For calls with no client library support yet.
        # Includes all headnode calls; registration of nodes and switches.
        http_client = RequestsHTTPClient()
        http_client.auth = (basic_username, basic_password)
        # For calls using the client library
        return Client(ep, http_client), http_client
    # Next try keystone:
    try:
        from keystoneauth1.identity import v3
        from keystoneauth1 import session
        os_auth_url = quads_config['OS_AUTH_URL']
        os_password = quads_config['OS_PASSWORD']
        os_username = quads_config['OS_USERNAME']
        os_user_domain_id = quads_config['OS_USER_DOMAIN_ID'] or 'default'
        os_project_name = quads_config['OS_PROJECT_NAME']
        os_project_domain_id = quads_config['OS_PROJECT_DOMAIN_ID'] or 'default'
        if None in (os_auth_url, os_username, os_password, os_project_name):
            raise KeyError("Required openstack environment variable not set.")
        auth = v3.Password(auth_url=os_auth_url,
                           username=os_username,
                           password=os_password,
                           project_name=os_project_name,
                           user_domain_id=os_user_domain_id,
                           project_domain_id=os_project_domain_id)
        sess = session.Session(auth=auth)
        http_client = KeystoneHTTPClient(sess)
        return Client(ep, http_client), http_client
    except (ImportError, KeyError):
        pass
    # Finally, fall back to no authentication:
    http_client = requests.Session()
    return Client(ep, http_client), http_client


client = setup_http_client()[0]
http_client = setup_http_client()[1]
