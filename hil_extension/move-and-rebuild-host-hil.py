#!/bin/python

import sys
import cli
import time

def move_host(argv):
    if len(argv) != 3:
        sys.exit("Incorrect number of arguments. Should be host_to_move old_cloud new_cloud.")
    host_to_move = argv[0]
    old_cloud = argv[1]
    new_cloud = argv[2]
    node_nics = cli.show_node(host_to_move)['nics']
    print("TESTING: Before move " + str(node_nics))
    for nic_json in node_nics:
        time.sleep(1)
        cli.node_detach_network(host_to_move,
                            nic_json['label'],
                            old_cloud)
        time.sleep(1)
        time.sleep(1)
        cli.node_connect_network(host_to_move,
                             nic_json['label'],
                             new_cloud,
                             'null')
        time.sleep(1)
    node_nics = cli.show_node(host_to_move)['nics']
    print("TESTING: After move " + str(node_nics))

if __name__ == "__main__":
   move_host(sys.argv[1:])
