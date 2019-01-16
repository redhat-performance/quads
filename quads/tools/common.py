import os
import requests

from quads.helpers import quads_load_config

conf_file = os.path.join(os.path.dirname(__file__), "../../conf/quads.yml")
conf = quads_load_config(conf_file)

API = 'v2'
API_URL = os.path.join(conf['quads_base_url'], 'api', API)


def environment_released(_owner, _env):
    _url = os.path.join(API_URL, "cloud")
    _response = requests.get(_url)
    ticket = ""
    if _response.status_code == 200:
        data = _response.json()
        if type(data) == list:
            for cloud in data:
                if cloud["name"] == _env:
                    ticket = cloud["ticket"]
                    break
    else:
        return False
    release_dir = os.path.join(conf["data_dir"], "release")
    release_file = os.path.join(release_dir, "%s-%s-%s" % (_env, _owner, ticket))
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    if os.path.exists(release_file):
        return True

    return False
