#!/bin/python
import sys
import json
import pprint
import os
import jinja2
#sys.path.append(quads_config["install_dir"] + "/lib")
#sys.path.append(os.path.dirname(__file__) + "/../lib")
#from Quads import Quads
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


# TODO(sai): these values for total node count should be passed to the script
inventory = {}
inventory['r930'] = 3
inventory['r730'] = 0
inventory['r630'] = 2
inventory['r620'] = 4
inventory['6048r'] = 0
inventory['6018r'] = 0

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
    priority_list = sorted(priority_dict.items(), key=lambda x: x[1], reverse=True)
    return priority_list



def schedule_nodes(count, priority, role=None):
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
    with open(fname) as instack_file:
        instack_data = json.load(instack_file)
    return instack_data
    #print instack_data['nodes']

def tag_instack(instack_data, nodes, role, quads, instack_file):
    for type, count in nodes.items():
        node_index = 0
        i = 0
        for machine in instack_data['nodes']:
        # TODO(sai): remove ugly hack to get node type, have node type as a filed
        # in instackenv.json populated during initial creation itself
        # uncomment below line to dynamically get machine type when done with
        # testing
            #machine_type = quads.get_host_type(machine['pm_addr'].split('-', 1)[1])
            machine_type = machine['pm_addr'].split('-')[3].split('.')[0]
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
    with open('sai.json', 'w') as instack:
        json.dump(instack_data, instack, indent=4)

def render(tpl_path, context):
    path, filename = os.path.split(os.path.abspath(os.path.expanduser(tpl_path)))
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
    return jinja_env.get_template(filename).render(context)


def quads_load_config(quads_config):
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
    config_file = os.path.dirname(__file__) + '/../conf/openstack.conf'
    cfg.CONF(default_config_files=[config_file])
    quads = initialize_quads_object()
    # TODO(sai): uncomment below lines to dynamically get inventory for the
    # cloud as we currently hardcoded inventory for testing purposes
    # global inventory 
    inventor = quads.query_cloud_host_types(None, cfg.CONF.cloud)
    print inventor
    # Remove undercloud from inventory
    # undercloud_type = quads.get_host_type(cfg.CONF.undercloud)
    # inventory[undercloud_type] -=1
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
    ceph_nodes = schedule_nodes(2, ceph_priority)
    compute_nodes = schedule_nodes(3, compute_priority)
    try:
        instack_data = load_json(cfg.CONF.instackenv)
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, controller_nodes, 'control', quads, cfg.CONF.instackenv)
    try:
        instack_data = load_json('sai.json')
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, compute_nodes, 'compute', quads, cfg.CONF.instackenv)
    try:
        instack_data = load_json('sai.json')
    except IOError:
        print("File {} doesn't exist").format(cfg.CONF.instackenv)
        sys.exit(1)
    tag_instack(instack_data, ceph_nodes, 'ceph', quads, cfg.CONF.instackenv)
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



