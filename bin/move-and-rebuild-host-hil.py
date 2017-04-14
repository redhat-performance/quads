#!/bin/python

import sys
import cli

def move_host(argv):
    host_to_move = argv[1]
    old_cloud = argv[2]
    new_cloud = argv[3]
    print(show_node(host_to_move))
    #node_name = show_node(host_to_move)['name']
    #node_nics = show_node(host_to_move)['nics']
    # for nic_json in node_nics:
    #     node_detach_network(node_name,
    #                         nic_json['label'],
    #                         old_cloud)
    #     node_connect_network(node_name,
    #                          nic_json['label'],
    #                          new_cloud)

if __name__ == "__main__":
   move_host(sys.argv)