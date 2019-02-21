import os
import yaml


def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError:
                print("quads: Invalid YAML config: " + quads_config)
                return
    except Exception as ex:
        print(ex)
        return
    return quads_config_yaml


quads_config_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(quads_config_file)

SUPPORTED = ["r620", "r630", "r720", "r730", "r930"]
OFFSETS = {"em1": 0, "em2": 1, "em3": 2, "em4": 3}
API = "v2"
API_URL = os.path.join(conf['quads_base_url'], 'api', API)
