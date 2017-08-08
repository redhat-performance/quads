#!/bin/python
import sys
import json
import pprint
import os
import jinja2
import config
import yaml
from oslo_config import cfg


# TODO(sai): Make these priorities dynamic based on Ansible facts
controller_priority={}
compute_priority={}
ceph_priority={}

controller_priority['r930'] = cfg.CONF.control.priority_r930
controller_priority['r730'] = cfg.CONF.control.priority_r730
controller_priority['r630'] = cfg.CONF.control.priority_r630
controller_priority['r620'] = cfg.CONF.control.priority_r620
controller_priority['6048r'] = cfg.CONF.control.priority_6048r
controller_priority['6018r'] = cfg.CONF.control.priority_6018r

# ceph priorities
ceph_priority['r930'] = cfg.CONF.control.priority_r930
ceph_priority['r730'] = cfg.CONF.control.priority_r730
ceph_priority['r630'] = cfg.CONF.control.priority_r630
ceph_priority['r620'] = cfg.CONF.control.priority_r620
ceph_priority['6048r'] = cfg.CONF.control.priority_6048r
ceph_priority['6018r'] = cfg.CONF.control.priority_6018r


# compute priorities
compute_priority['r930'] = cfg.CONF.control.priority_r930
compute_priority['r730'] = cfg.CONF.control.priority_r730
compute_priority['r630'] = cfg.CONF.control.priority_r630
compute_priority['r620'] = cfg.CONF.control.priority_r620
compute_priority['6048r'] = cfg.CONF.control.priority_6048r
compute_priority['6018r'] = cfg.CONF.control.priority_6018r



# role node counts
composable_role = {}
composable_role['control'] = 0
composable_role['r620compute'] = 0
composable_role['r630compute'] = 0
composable_role['r730compute'] = 0
composable_role['6048rcompute'] = 0
composable_role['6018rcompute'] = 0
composable_role['r930compute'] = 0
composable_role['r620ceph'] = 0
composable_role['r630ceph'] = 0
composable_role['r730ceph'] = 0
composable_role['6048rceph'] = 0
composable_role['6018rceph'] = 0
composable_role['r930ceph'] = 0


# keys in priority dictionary and inventory dictionary should be the same for the
# sorting to be possbile 

def sort_priority(priority_dict):
    """Sorts priority the node types according to priority.

    This function takes the dictionary of host types and priorities as input and return a list
    of (nodetype, priority) tuples in the order of priorites

    :param priority_dict: dictionary of hosttype, priorities

    :returns: sorted list of (nodetype, priority) tuples in descending order
    """
    priority_list = sorted(priority_dict.items(), key=lambda x: x[1], reverse=True)
    return priority_list



def schedule_nodes(count, priority, role=None):
    """Schedules different node types into OpenStack roles.

    This function schedules the different node types available into roles so
    that they can be tagged with the appropriate profile later on for
    deployment. It returns the number of node of each nodetype that can be used
    for a particular role.

    :param count: integer number of nodes of that role that need to be scheduled
    :param priority: dictionary of nodettype, priority for this particular
    role
    :param: role: string, the OpenStack role we want to schedule nodes as, is
    generally one of control, compute and ceph

    :returns: dictionary of nodetype, number
    """
    systems = {}
    filter = sort_priority(priority)
    if sum(inventory.values()) < count:
        sys.exit(1)
    # NOTE(sai): we need role_minimum as controller node is not composable and we
    # need to check if a minimum of 3 nodes if that node type is to be scheduled
    # as controllers
    role_minimum = 2 if role == 'control' else 0
    for type, weight in filter:
        if inventory[type] > role_minimum:
            # keys in inventory dictionary and priority dictionary should be same
            for i in range(0, count):
                if inventory[type] > 0:
                    systems[type] = systems.get(type, 0) + 1
                    count -= 1
                    inventory[type] -= 1
    return systems



def load_json(fname):
    """Loads the JSON file.

    This function is used to load a JSON file into a dictionary

    :param fname: name of the file to load

    :returns: dictionary of the JSON contents
    """
    with open(fname) as instack_file:
        instack_data = json.load(instack_file)
    return instack_data

def tag_instack(instack_data, nodes, role, quads, instack_file):
    """Tags the isntack file with appropriate names.

    This function tags  each node of the isntack file with a name key that can
    be used by infrared to associate a node with a flavor. For example, if a
    node is tagged with a string such as r630compute-0, infrared strip
    everything following the creates an r630compute flavor and tags this node
    with  the r630compute profile. This kind of mapping is required to deploy
    with composable roles successfully.

    :param instack_data: the dictionary loaded from the isntack file
    :param nodes: dictionary of nodetype, number for this role
    :param role: the OpenStack role, one of control, compute or ceph
    :param quads: the quads object, used to query node type of each machine
    :param instack_file: the instack file to write the name tags to
    """
    for type, count in nodes.items():
        node_index = 0
        for machine in instack_data['nodes']:
            machine_type = quads.get_host_type(machine['pm_addr'].split('-', 1)[1])
            if ( 'name' not in machine and machine_type in nodes and
            nodes[machine_type] > 0  and type == machine_type):
                if role == 'control':
                    machine['name'] = role + '-' + str(node_index)
                    composable_role[role]+=1
                else:
                    machine['name'] = machine_type + role + '-' + str(node_index)
                    composable_role[machine_type+role]+=1
                node_index = node_index + 1
                nodes[machine_type] -= 1
    dump_json(instack_data, instack_file)

def dump_json(instack_data, instack_file):
    """Dumps dictionary to JSON file

    This function dumps a given dictionary to a JSON file on the filesystem

    :param instack_data: dictionary of instack data
    :param instack_file: the file to write the instack_data dictionary to
    """
    with open(instack_file, 'w') as instack:
        json.dump(instack_data, instack, indent=4)

def render(tpl_path, context):
    """Render a template

    This function renders a template with the given variables

    :param tpl_path: the path to the template file
    :param context: dictionary of variablename, value to replace in the template
    """
    path, filename = os.path.split(os.path.abspath(os.path.expanduser(tpl_path)))
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
    return jinja_env.get_template(filename).render(context)


def quads_load_config(quads_config):
    """Loads the QUADS config file

    This function loads the configuration file for QUADS

    :param quads_config: name of the configuration file

    :returns: dictionary of the configuration options
    """
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except Exception, ex:
                print "quads: Invalid YAML config: " + quads_config
                print ex
                exit(1)
    except Exception, ex:
        print ex
        exit(1)
    return(quads_config_yaml)


def initialize_quads_object():
    """Initializes the QUADS object

    This function is used to initialize the QUADS object which is later used to
    query information regarding the cloud.
    """
    quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads_config = quads_load_config(quads_config_file)
    defaultconfig = quads_config["data_dir"] + "/schedule.yaml"
    defaultstatedir = quads_config["data_dir"] + "/state"
    sys.path.append(quads_config["install_dir"] + "/lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib")
    from Quads import Quads
    quads = Quads(defaultconfig, defaultstatedir)
    return quads

def query_openstack_config(quads, cloud_name, property):
    """Query the OpenStack configuration for cloud

    This function queries the OpenStack  configuration that needs to be deployed
    for the cloud. The version, build, various role counts are queried.

    :param quads: the quads object used to query information from schedule YAML
    :param cloud_name: the name of the cloud to query information for
    :param property: the property to query for, could be one of version, build,
    controller count, compute count or ceph count

    :returns: string, the value queried for
    """
    value = None
    openstack_clouds = quads.query_cloud_postconfig(None, True, ['openstack'])
    for cloud in openstack_clouds:
        for cloudname, details in cloud.iteritems():
            if cloudname == cloud_name:
                for service in  details.get('post_config'):
                    if service['name'] =='openstack':
                        value = service[property]
    return value


def main():
    """Main function that generates the instackenv

    This function makes use of all the other functions to assign each available
    machine in the cloud to an OpenStack role based on requirements. It
    ultimately generates the instackenv, network-environment.yaml and
    nic-configs  that can be consumed by infrared.
    """
    config_file = os.path.dirname(__file__) + '/../conf/openstack.conf'
    cfg.CONF(default_config_files=[config_file])
    quads = initialize_quads_object()
    global inventory
    inventory = quads.query_cloud_host_types(None, cfg.CONF.cloud)
    undercloud_type = quads.get_host_type(cfg.CONF.undercloud)
    inventory[undercloud_type] -=1
    version = query_openstack_config(quads, cfg.CONF.cloud, 'version')
    build = query_openstack_config(quads, cfg.CONF.cloud, 'build')
    if cfg.CONF.query:
        print version
        print build
        sys.exit(0)
    if not os.path.isfile(cfg.CONF.instackenv):
        sys.exit(1)
    if not os.path.isdir(cfg.CONF.templates):
        sys.exit(1)
    controller_count = query_openstack_config(quads, cfg.CONF.cloud,
                                              'controllers')
    compute_count = query_openstack_config(quads, cfg.CONF.cloud, 'computes')
    ceph_count = query_openstack_config(quads, cfg.CONF.cloud, 'ceph')
    # Schedule in the order of controller, ceph and compute
    controller_nodes = schedule_nodes(controller_count, controller_priority, 'control')
    ceph_nodes = schedule_nodes(ceph_count, ceph_priority)
    compute_nodes = schedule_nodes(compute_count, compute_priority)
    try:
        instack_data = load_json(cfg.CONF.instackenv)
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, controller_nodes, 'control', quads, (os.path.join(cfg.CONF.templates,'instackenv.json'))
    try:
        instack_data = load_json(os.path.join(cfg.CONF.templates,'instackenv.json'))
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, compute_nodes, 'compute', quads, (os.path.join(cfg.CONF.templates,'instackenv.json'))
    try:
        instack_data = load_json(os.path.join(cfg.CONF.templates,'instackenv.json'))
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, ceph_nodes, 'ceph', quads, (os.path.join(cfg.CONF.templates,'instackenv.json'))
    for type, count in controller_nodes.iteritems():
        controller_type = type
    controller = {'type': controller_type}
    deploy = {'controller_count': composable_role['control'],
              'r930compute_count': composable_role['r930compute'],
              'r730compute_count': composable_role['r730compute'],
              'r630compute_count': composable_role['r630compute'],
              'r620compute_count': composable_role['r620compute'],
              'r6048compute_count': composable_role['6048rcompute'],
              'r6018compute_count': composable_role['6018rcompute'],
              'r930ceph_count': composable_role['r930ceph'],
              'r730ceph_count': composable_role['r730ceph'],
              'r630ceph_count': composable_role['r630ceph'],
              'r620ceph_count': composable_role['r620ceph'],
              'r6048ceph_count': composable_role['6048rceph'],
              'r6018ceph_count': composable_role['6018rceph']
              }
    deploy_template = os.path.join(cfg.CONF.templates, 'deploy.yaml.j2')
    overcloud_script_template = os.path.join(cfg.CONF.templates, 'overcloud_deploy.sh.j2')
    deploy_file = os.path.join(cfg.CONF.templates, 'deploy.yaml')
    overcloud_script_file = os.path.join(cfg.CONF.templates, 'overcloud_deploy.sh')
    network_environment_template = os.path.join(cfg.CONF.templates, 'network-environment.yaml.j2')
    network_environment_file = os.path.join(cfg.CONF.templates, 'network-environment.yaml')
    with open(deploy_file, 'w') as f:
        result = render(deploy_template, deploy)
        f.write(result)
    with open(network_environment_file, 'w') as f:
        result = render(network_environment_template, controller)
        f.write(result)
    context = {'version': version}
    with open(overcloud_script_file, 'w') as f:
        result = render(overcloud_script_template, context)
        f.write(result)
if __name__ == '__main__':
    sys.exit(main())

