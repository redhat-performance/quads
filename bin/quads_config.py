#!/usr/bin/env python
import yaml 
import sys

# used to load the configuration for quads behavior
def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except Exception, ex:
 #               print "quads: Invalid YAML config: " + quads_config
                sys.exit("quads: Invalid YAML config: " + quads_config)
    except Exception, ex:
        print ex
        sys.exit(1)
    return(quads_config_yaml)
