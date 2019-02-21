import os
import yaml


def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError:
                print("quads: Invalid YAML config: " + quads_config)
                exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    return quads_config_yaml


quads_config_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(quads_config_file)
