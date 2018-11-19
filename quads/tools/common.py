import os

from helpers import quads_load_config
from util import get_tickets

conf_file = os.path.join(os.path.dirname(__file__), "../../conf/quads.yml")
conf = quads_load_config(conf_file)


def environment_released(_quads, _owner, _env):
    ticket = get_tickets(_quads, _env)
    release_dir = os.path.join(conf["data_dir"], "release")
    release_file = os.path.join(release_dir, "%s-%s-%s" % (_env, _owner, ticket))
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    if os.path.exists(release_file):
        return True

    return False
