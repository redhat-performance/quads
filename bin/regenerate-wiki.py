#!/usr/bin/env python

import os
from . import create_input
from quads.helpers import quads_load_config


conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)

quads = conf["install_dir"] + "/bin/quads-cli"
data_dir = conf["data_dir"]
bin_dir = conf["install_dir"] + "/bin"
wp_wiki = conf["wp_wiki"]
wp_username = conf["wp_username"]
wp_password = conf["wp_password"]
wp_wiki_main_title = conf["wp_wiki_main_title"]
wp_wiki_main_page_id = conf["wp_wiki_main_page_id"]
wp_wiki_assignments_title = conf["wp_wiki_assignments_title"]
wp_wiki_assignments_page_id = conf["wp_wiki_assignments_page_id"]
wp_wiki_git_manage = conf["wp_wiki_git_manage"]
wp_wiki_git_repo_path = conf["wp_wiki_git_repo_path"]

lockfile = data_dir + "/.wiki_regenerate"
quads_url = conf["quads_url"]
rt_url = conf["rt_url"]
exclude_hosts = conf["exclude_hosts"]
domain = conf["domain"]
racks = conf["racks"]


if __name__ == "__main__":
    create_input.main()
    if wp_wiki_git_manage:
        if os.path.exists(wp_wiki_git_repo_path):
            pass
