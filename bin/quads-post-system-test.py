#!/usr/bin/env python

import argparse
import os
import requests
import sys
import yaml


# used to load the configuration for quads behavior
def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError:
                print "quads: Invalid YAML config: " + quads_config
                exit(1)
    except Exception as ex:
        print ex
        exit(1)
    return quads_config_yaml


def main():
    quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads_config = quads_load_config(quads_config_file)

    requests.packages.urllib3.disable_warnings()

    if "data_dir" not in quads_config:
        print "quads: Missing \"data_dir\" in " + quads_config_file
        exit(1)

    if "install_dir" not in quads_config:
        print "quads: Missing \"install_dir\" in " + quads_config_file
        exit(1)

    if "quads_base_url" not in quads_config:
        print "quads: Missing \"quads_base_url\" in " + quads_config_file
        exit(1)

    sys.path.append(quads_config["install_dir"] + "/lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib")
    from requests.auth import HTTPBasicAuth

    parser = argparse.ArgumentParser(description='Query current hosts marked for build')
    parser.add_argument('--cloud', dest='cloud', type=str, default=None, help='specify the cloud to query')

    args = parser.parse_args()

    exitcode = 0
    # need to determine the ticket / password
    if args.cloud:
        # post
        url = quads_config["quads_base_url"] + "api/v1/lstickets"
        headers = {'Content-Type': 'application/json'}
        data = {"cloudonly": args.cloud}
        r = requests.post(url, data, headers=headers)
        js = r.json()
        if 'ticket' in js:
            if len(js['ticket']) == 0:
                ticket_value = None
            for owner in js['ticket']:
                ticket_value = owner[args.cloud]

        if not ticket_value:
            ticket_value = quads_config['ipmi_password']
        url = quads_config['foreman_api_url'] + "/hosts?search=build=true"
        headers = {'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers,
                         auth=HTTPBasicAuth(args.cloud, ticket_value),
                         verify=False)
        js = r.json()
        if 'results' not in js:
            print "Unable to query foreman for cloud: " + args.cloud
            print "Verify foreman password is correct: " + ticket_value
            exitcode = 1
        else:
            if len(js['results']) > 0:
                print "The following hosts are marked for build:"
                print ""
            for h in js['results']:
                print h['name']
                exitcode = 1

    exit(exitcode)


if __name__ == "__main__":
    main()
