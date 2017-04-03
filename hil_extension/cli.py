#!/bin/python

# Copyright 2013-2014 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

"""This module implements the HaaS command line tool."""
import inspect
import json
import os
import requests
import sys
import urllib
import abc
import yaml
import json

from functools import wraps

command_dict = {}
usage_dict = {}
MIN_PORT_NUMBER = 1
MAX_PORT_NUMBER = 2**16 - 1


class HTTPClient(object):
    """An HTTP client.

    Makes HTTP requests on behalf of the HaaS CLI. Responsible for adding
    authentication information to the request.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request(method, url, data=None, params=None):
        """Make an HTTP request

        Makes an HTTP request on URL `url` with method `method`, request body
        `data`(if supplied) and query parameter `params`(if supplied). May add
        authentication or other backend-specific information to the request.

        Parameters
        ----------

        method : str
            The HTTP method to use, e.g. 'GET', 'PUT', 'POST'...
        url : str
            The URL to act on
        data : str, optional
            The body of the request
        params : dictionary, optional
            The query parameter, e.g. {'key1': 'val1', 'key2': 'val2'},
            dictionary key can't be `None`

        Returns
        -------

        requests.Response
            The HTTP response
        """


class RequestsHTTPClient(requests.Session, HTTPClient):
    """An HTTPClient which uses the requests library.

    Note that this doesn't do anything over `requests.Session`; that
    class already implements the required interface. We declare it only
    for clarity.
    """


class KeystoneHTTPClient(HTTPClient):
    """An HTTPClient which authenticates with Keystone.

    This uses an instance of python-keystoneclient's Session class
    to do its work.
    """

    def __init__(self, session):
        """Create a KeystoneHTTPClient

        Parameters
        ----------

        session : keystoneauth1.Session
            A keystone session to make the requests with
        """
        self.session = session

    def request(self, method, url, data=None, params=None):
        """Make an HTTP request using keystone for authentication.

        Smooths over the differences between python-keystoneclient's
        request method that specified by HTTPClient
        """
        # We have to import this here, since we can't assume the library
        # is available from global scope.
        from keystoneauth1.exceptions.http import HttpError

        try:
            # The order of these parameters is different that what
            # we expect, but the names are the same:
            return self.session.request(method=method,
                                        url=url,
                                        data=data,
                                        params=params)
        except HttpError as e:
            return e.response


# An instance of HTTPClient, which will be used to make the request.
http_client = None


class InvalidAPIArgumentsException(Exception):
    pass


def cmd(f):
    """A decorator for CLI commands.

    This decorator firstly adds the function to a dictionary of valid CLI
    commands, secondly adds exception handling for when the user passes the
    wrong number of arguments, and thirdly generates a 'usage' description and
    puts it in the usage dictionary.
    """

    # Build the 'usage' info for the help:
    args, varargs, _, _ = inspect.getargspec(f)
    num_args = len(args)  # used later to validate passed args.
    showee = [f.__name__] + ['<%s>' % name for name in args]
    args = ' '.join(['<%s>' % name for name in args])
    if varargs:
        showee += ['<%s...>' % varargs]
    usage_dict[f.__name__] = ' '.join(showee)

    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            # For commands which accept a variable number of arguments,
            # num_args is the *minimum* required arguments; there is no
            # maximum. For other commands, there must be *exactly* `num_args`
            # arguments:
            if len(args) < num_args or not varargs and len(args) > num_args:
                raise InvalidAPIArgumentsException()
            f(*args, **kwargs)
        except InvalidAPIArgumentsException as e:
            if e.message != '':
                sys.stderr.write(e.message + '\n\n')
            sys.stderr.write('Invalid arguements.  Usage:\n')
            help(f.__name__)

    command_dict[f.__name__] = wrapped
    return wrapped


def setup_http_client():
    """Set `http_client` to a valid instance of `HTTPClient`

    Sets http_client to an object which makes HTTP requests with
    authentication. It chooses an authentication backend as follows:

    1. If the environment variables HAAS_USERNAME and HAAS_PASSWORD
       are defined, it will use HTTP basic auth, with the corresponding
       user name and password.
    2. If the `python-keystoneclient` library is installed, and the
       environment variables:

           * OS_AUTH_URL
           * OS_USERNAME
           * OS_PASSWORD
           * OS_PROJECT_NAME

       are defined, Keystone is used.
    3. Oterwise, do not supply authentication information.

    This may be extended with other backends in the future.
    """
    global http_client
    # First try basic auth:
    basic_username = os.getenv('HAAS_USERNAME')
    basic_password = os.getenv('HAAS_PASSWORD')
    if basic_username is not None and basic_password is not None:
        http_client = RequestsHTTPClient()
        http_client.auth = (basic_username, basic_password)
        return
    # Next try keystone:
    try:
        from keystoneauth1.identity import v3
        from keystoneauth1 import session
        os_auth_url = os.getenv('OS_AUTH_URL')
        os_password = os.getenv('OS_PASSWORD')
        os_username = os.getenv('OS_USERNAME')
        os_user_domain_id = os.getenv('OS_USER_DOMAIN_ID') or 'default'
        os_project_name = os.getenv('OS_PROJECT_NAME')
        os_project_domain_id = os.getenv('OS_PROJECT_DOMAIN_ID') or 'default'
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
        return
    except (ImportError, KeyError):
        pass
    # Finally, fall back to no authentication:
    http_client = requests.Session()


class FailedAPICallException(Exception):
    pass


def check_status_code(response):
    if response.status_code < 200 or response.status_code >= 300:
        sys.stderr.write('Unexpected status code: %d\n' % response.status_code)
        sys.stderr.write('Response text:\n')
        sys.stderr.write(response.text + "\n")
        raise FailedAPICallException()
    else:
        sys.stdout.write(response.text + "\n")
    return response

# TODO: This function's name is no longer very accurate.  As soon as it is
# safe, we should change it to something more generic.
def object_url(*args):
    # Prefer an environmental variable for getting the endpoint if available.
    with open("hil.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError:
            sys.exit("Can't parse hil.yml file.")
    url = data.get('url')
    if url is None:
        sys.exit("Hil url is not specified in hil.yml.")

    for arg in args:
        url += '/' + urllib.quote(arg, '')
    return url


# Helper functions for making HTTP requests against the API.
#    Uses the global variable `http_client` to make the request.
#
#    Arguments:
#
#        `url` - The url to make the request to
#        `data` - the body of the request (for PUT, POST and DELETE)
#        `params` - query parameters (for GET)

def do_put(url, data={}):
    check_status_code(requests.request('PUT', url, data=json.dumps(data)))


def do_post(url, data={}):
    check_status_code(requests.request('POST', url, data=json.dumps(data)))


def do_get(url, params=None):
    return check_status_code(requests.get(url, params=params)).json()

def do_delete(url):
    check_status_code(requests.request('DELETE', url))


@cmd
def serve(port):
    try:
        port = schema.And(
            schema.Use(int),
            lambda n: MIN_PORT_NUMBER <= n <= MAX_PORT_NUMBER).validate(port)
    except schema.SchemaError:
        raise InvalidAPIArgumentsException(
            'Error: Invaid port. Must be in the range 1-65535.'
        )
    except Exception as e:
        sys.exit('Unxpected Error!!! \n %s' % e)

    """Start the HaaS API server"""
    if cfg.has_option('devel', 'debug'):
        debug = cfg.getboolean('devel', 'debug')
    else:
        debug = False
    # We need to import api here so that the functions within it get registered
    # (via `rest_call`), though we don't use it directly:
    from haas import model, api, rest
    server.init()
    migrations.check_db_schema()
    server.stop_orphan_consoles()
    rest.serve(port, debug=debug)

@cmd
def serve_networks():
    """Start the HaaS networking server"""
    from haas import model, deferred
    from time import sleep
    server.init()
    server.register_drivers()
    server.validate_state()
    model.init_db()
    migrations.check_db_schema()
    while True:
        # Empty the journal until it's empty; then delay so we don't tight
        # loop.
        while deferred.apply_networking():
            pass
        sleep(2)


@cmd
def user_create(username, password, is_admin):
    """Create a user <username> with password <password>.
    <is_admin> may be either "admin" or "regular", and determines whether
    the user has administrative priveledges.
    """
    url = object_url('/auth/basic/user', username)
    if is_admin not in ('admin', 'regular'):
        raise InvalidAPIArgumentsException(
            "is_admin must be either 'admin' or 'regular'"
        )
    do_put(url, data={
        'password': password,
        'is_admin': is_admin == 'admin',
    })


@cmd
def network_create(network, owner, access, net_id):
    """Create a link-layer <network>.  See docs/networks.md for details"""
    url = object_url('network', network)
    do_put(url, data={'owner': owner,
                      'access': access,
                      'net_id': net_id})


@cmd
def network_create_simple(network, project):
    """Create <network> owned by project.  Specific case of network_create"""
    url = object_url('network', network)
    do_put(url, data={'owner': project,
                      'access': project,
                      'net_id': ""})


@cmd
def network_delete(network):
    """Delete a <network>"""
    url = object_url('network', network)
    do_delete(url)


@cmd
def user_delete(username):
    """Delete the user <username>"""
    url = object_url('/auth/basic/user', username)
    do_delete(url)


@cmd
def list_projects():
    """List all projects"""
    url = object_url('projects')
    do_get(url)


@cmd
def user_add_project(user, project):
    """Add <user> to <project>"""
    url = object_url('/auth/basic/user', user, 'add_project')
    do_post(url, data={'project': project})


@cmd
def user_remove_project(user, project):
    """Remove <user> from <project>"""
    url = object_url('/auth/basic/user', user, 'remove_project')
    do_post(url, data={'project': project})


@cmd
def network_grant_project_access(project, network):
    """Add <project> to <network> access"""
    url = object_url('network', network, 'access', project)
    do_put(url)


@cmd
def network_revoke_project_access(project, network):
    """Remove <project> from <network> access"""
    url = object_url('network', network, 'access', project)
    do_delete(url)


@cmd
def project_create(project):
    """Create a <project>"""
    url = object_url('project', project)
    do_put(url)


@cmd
def project_delete(project):
    """Delete <project>"""
    url = object_url('project', project)
    do_delete(url)


@cmd
def headnode_create(headnode, project, base_img):
    """Create a <headnode> in a <project> with <base_img>"""
    url = object_url('headnode', headnode)
    do_put(url, data={'project': project,
                      'base_img': base_img})


@cmd
def headnode_delete(headnode):
    """Delete <headnode>"""
    url = object_url('headnode', headnode)
    do_delete(url)


@cmd
def project_connect_node(project, node):
    """Connect <node> to <project>"""
    url = object_url('project', project, 'connect_node')
    do_post(url, data={'node': node})


@cmd
def project_detach_node(project, node):
    """Detach <node> from <project>"""
    url = object_url('project', project, 'detach_node')
    do_post(url, data={'node': node})


@cmd
def headnode_start(headnode):
    """Start <headnode>"""
    url = object_url('headnode', headnode, 'start')
    do_post(url)


@cmd
def headnode_stop(headnode):
    """Stop <headnode>"""
    url = object_url('headnode', headnode, 'stop')
    do_post(url)


@cmd
def node_register(node, subtype, *args):
    """Register a node named <node>, with the given type
        if obm is of type: ipmi then provide arguments
        "ipmi", <hostname>, <ipmi-username>, <ipmi-password>
    """
    obm_api = "http://schema.massopencloud.org/haas/v0/obm/"
    obm_types = ["ipmi", "mock"]
    # Currently the classes are hardcoded
    # In principle this should come from api.py
    # In future an api call to list which plugins are active will be added.

    if subtype in obm_types:
        if len(args) == 3:
            obminfo = {"type": obm_api + subtype, "host": args[0],
                       "user": args[1], "password": args[2]
                       }
        else:
            sys.stderr.write('ERROR: subtype ' + subtype +
                             ' requires exactly 3 arguments\n')
            sys.stderr.write('<hostname> <ipmi-username> <ipmi-password>\n')
            return
    else:
        sys.stderr.write('ERROR: Wrong OBM subtype supplied\n')
        sys.stderr.write('Supported OBM sub-types: ipmi, mock\n')
        return

    url = object_url('node', node)
    do_put(url, data={"obm": obminfo})


@cmd
def node_delete(node):
    """Delete <node>"""
    url = object_url('node', node)
    do_delete(url)


@cmd
def node_power_cycle(node):
    """Power cycle <node>"""
    url = object_url('node', node, 'power_cycle')
    do_post(url)


@cmd
def node_power_off(node):
    """Power off <node>"""
    url = object_url('node', node, 'power_off')
    do_post(url)


@cmd
def node_set_bootdev(node, dev):
    """
    Sets <node> to boot from <dev> persistenly
    eg; haas node_set_bootdev dell-23 pxe
    for IPMI, dev can be set to disk, pxe, or none
    """
    url = object_url('node', node, 'boot_device')
    do_put(url, data={'bootdev': dev})


@cmd
def node_register_nic(node, nic, macaddr):
    """
    Register existence of a <nic> with the given <macaddr> on the given <node>
    """
    url = object_url('node', node, 'nic', nic)
    do_put(url, data={'macaddr': macaddr})


@cmd
def node_delete_nic(node, nic):
    """Delete a <nic> on a <node>"""
    url = object_url('node', node, 'nic', nic)
    do_delete(url)


@cmd
def headnode_create_hnic(headnode, nic):
    """Create a <nic> on the given <headnode>"""
    url = object_url('headnode', headnode, 'hnic', nic)
    do_put(url)


@cmd
def headnode_delete_hnic(headnode, nic):
    """Delete a <nic> on a <headnode>"""
    url = object_url('headnode', headnode, 'hnic', nic)
    do_delete(url)


@cmd
def node_connect_network(node, nic, network, channel):
    """Connect <node> to <network> on given <nic> and <channel>"""
    url = object_url('node', node, 'nic', nic, 'connect_network')
    do_post(url, data={'network': network,
                       'channel': channel})


@cmd
def node_detach_network(node, nic, network):
    """Detach <node> from the given <network> on the given <nic>"""
    url = object_url('node', node, 'nic', nic, 'detach_network')
    do_post(url, data={'network': network})


@cmd
def headnode_connect_network(headnode, nic, network):
    """Connect <headnode> to <network> on given <nic>"""
    url = object_url('headnode', headnode, 'hnic', nic, 'connect_network')
    do_post(url, data={'network': network})


@cmd
def headnode_detach_network(headnode, hnic):
    """Detach <headnode> from the network on given <nic>"""
    url = object_url('headnode', headnode, 'hnic', hnic, 'detach_network')
    do_post(url)


@cmd
def metadata_set(node, label, value):
    """Register metadata with <label> and <value> with <node> """
    url = object_url('node', node, 'metadata', label)
    do_put(url, data={'value': value})


@cmd
def metadata_delete(node, label):
    """Delete metadata with <label> from a <node>"""
    url = object_url('node', node, 'metadata', label)
    do_delete(url)


@cmd
def switch_register(switch, subtype, *args):
    """Register a switch with name <switch> and
    <subtype>, <hostname>, <username>,  <password>
    eg. haas switch_register mock03 mock mockhost01 mockuser01 mockpass01
    FIXME: current design needs to change. CLI should not know about every
    backend. Ideally, this should be taken care of in the driver itself or
    client library (work-in-progress) should manage it.
    """
    switch_api = "http://schema.massopencloud.org/haas/v0/switches/"
    if subtype == "nexus":
        if len(args) == 4:
            switchinfo = {
                "type": switch_api + subtype,
                "hostname": args[0],
                "username": args[1],
                "password": args[2],
                "dummy_vlan": args[3]}
        else:
            sys.stderr.write('ERROR: subtype ' + subtype +
                             ' requires exactly 4 arguments\n'
                             '<hostname> <username> <password>'
                             '<dummy_vlan_no>\n')
            return
    elif subtype == "mock":
        if len(args) == 3:
            switchinfo = {"type": switch_api + subtype, "hostname": args[0],
                          "username": args[1], "password": args[2]}
        else:
            sys.stderr.write('ERROR: subtype ' + subtype +
                             ' requires exactly 3 arguments\n')
            sys.stderr.write('<hostname> <username> <password>\n')
            return
    elif subtype == "powerconnect55xx":
        if len(args) == 3:
            switchinfo = {"type": switch_api + subtype, "hostname": args[0],
                          "username": args[1], "password": args[2]}
        else:
            sys.stderr.write('ERROR: subtype ' + subtype +
                             ' requires exactly 3 arguments\n'
                             '<hostname> <username> <password>\n')
            return
    elif subtype == "brocade":
        if len(args) == 4:
            switchinfo = {"type": switch_api + subtype, "hostname": args[0],
                          "username": args[1], "password": args[2],
                          "interface_type": args[3]}
        else:
            sys.stderr.write('ERROR: subtype ' + subtype +
                             ' requires exactly 4 arguments\n'
                             '<hostname> <username> <password> '
                             '<interface_type>\n'
                             'NOTE: interface_type refers '
                             'to the speed of the switchports\n '
                             'ex. TenGigabitEthernet, FortyGigabitEthernet, '
                             'etc.\n')
            return
    else:
        sys.stderr.write('ERROR: Invalid subtype supplied\n')
        return
    url = object_url('switch', switch)
    do_put(url, data=switchinfo)


@cmd
def switch_delete(switch):
    """Delete a <switch> """
    url = object_url('switch', switch)
    do_delete(url)


@cmd
def list_switches():
    """List all switches"""
    url = object_url('switches')
    do_get(url)


@cmd
def port_register(switch, port):
    """Register a <port> with <switch> """
    url = object_url('switch', switch, 'port', port)
    do_put(url)


@cmd
def port_delete(switch, port):
    """Delete a <port> from a <switch>"""
    url = object_url('switch', switch, 'port', port)
    do_delete(url)


@cmd
def port_connect_nic(switch, port, node, nic):
    """Connect a <port> on a <switch> to a <nic> on a <node>"""
    url = object_url('switch', switch, 'port', port, 'connect_nic')
    do_post(url, data={'node': node, 'nic': nic})


@cmd
def port_detach_nic(switch, port):
    """Detach a <port> on a <switch> from whatever's connected to it"""
    url = object_url('switch', switch, 'port', port, 'detach_nic')
    do_post(url)


@cmd
def list_network_attachments(network, project):
    """List nodes connected to a network
    <project> may be either "all" or a specific project name.
    """
    url = object_url('network', network, 'attachments')

    if project == "all":
        do_get(url)
    else:
        do_get(url, params={'project': project})


@cmd
def list_nodes(is_free):
    """List all nodes or all free nodes
    <is_free> may be either "all" or "free", and determines whether
        to list all nodes or all free nodes.
    """
    if is_free not in ('all', 'free'):
        raise InvalidAPIArgumentsException(
            "is_free must be either 'all' or 'free'"
        )
    url = object_url('nodes', is_free)
    do_get(url)


@cmd
def list_project_nodes(project):
    """List all nodes attached to a <project>"""
    url = object_url('project', project, 'nodes')
    do_get(url)


@cmd
def list_project_networks(project):
    """List all networks attached to a <project>"""
    url = object_url('project', project, 'networks')
    do_get(url)


@cmd
def show_switch(switch):
    """Display information about <switch>"""
    url = object_url('switch', switch)
    do_get(url)


@cmd
def list_networks():
    """List all networks"""
    url = object_url('networks')
    do_get(url)


@cmd
def show_network(network):
    """Display information about <network>"""
    url = object_url('network', network)
    do_get(url)


def show_node(node):
    """Display information about a <node>"""
    url = object_url('node', node)
    return do_get(url)


@cmd
def list_project_headnodes(project):
    """List all headnodes attached to a <project>"""
    url = object_url('project', project, 'headnodes')
    do_get(url)


@cmd
def show_headnode(headnode):
    """Display information about a <headnode>"""
    url = object_url('headnode', headnode)
    do_get(url)


@cmd
def list_headnode_images():
    """Display registered headnode images"""
    url = object_url('headnode_images')
    do_get(url)


@cmd
def show_console(node):
    """Display console log for <node>"""
    url = object_url('node', node, 'console')
    do_get(url)


@cmd
def start_console(node):
    """Start logging console output from <node>"""
    url = object_url('node', node, 'console')
    do_put(url)


@cmd
def stop_console(node):
    """Stop logging console output from <node> and delete the log"""
    url = object_url('node', node, 'console')
    do_delete(url)


@cmd
def create_admin_user(username, password):
    """Create an admin user. Only valid for the database auth backend.
    This must be run on the HaaS API server, with access to haas.cfg and the
    database. It will create an user named <username> with password
    <password>, who will have administrator priviledges.
    This command should only be used for bootstrapping the system; once you
    have an initial admin, you can (and should) create additional users via
    the API.
    """
    if not config.cfg.has_option('extensions', 'haas.ext.auth.database'):
        sys.exit("'make_inital_admin' is only valid with the database auth"
                 " backend.")
    from haas import model
    from haas.model import db
    from haas.ext.auth.database import User
    model.init_db()
    db.session.add(User(label=username, password=password, is_admin=True))
    db.session.commit()


@cmd
def help(*commands):
    """Display usage of all following <commands>, or of all commands if none
    are given
    """
    if not commands:
        sys.stdout.write('Usage: %s <command> <arguments...> \n' % sys.argv[0])
        sys.stdout.write('Where <command> is one of:\n')
        commands = sorted(command_dict.keys())
    for name in commands:
        # For each command, print out a summary including the name, arguments,
        # and the docstring (as a #comment).
        sys.stdout.write('  %s\n' % usage_dict[name])
        sys.stdout.write('      %s\n' % command_dict[name].__doc__)


def main():
    """Entry point to the CLI.
    There is a script located at ${source_tree}/scripts/haas, which invokes
    this function.
    """

    if len(sys.argv) < 2 or sys.argv[1] not in command_dict:
        # Display usage for all commands
        help()
        sys.exit(1)
    else:
        setup_http_client()
        try:
            command_dict[sys.argv[1]](*sys.argv[2:])
        except FailedAPICallException:
            sys.exit(1)
        except InvalidAPIArgumentsException:
            sys.exit(2)

if __name__ == "__main__":
   main()
