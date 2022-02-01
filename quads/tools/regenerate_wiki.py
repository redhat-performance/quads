#!/usr/bin/python3
import logging
import os
import ssl

from datetime import datetime
from xmlrpc.client import ProtocolError
from git import Repo, InvalidGitRepositoryError
from quads.config import conf
from quads.tools import create_input, create_input_assignments, racks_wiki
from quads.tools.regenerate_vlans_wiki import regenerate_vlans_wiki

wp_wiki = conf["wp_wiki"]
wp_username = conf["wp_username"]
wp_password = conf["wp_password"]
wp_wiki_main_title = conf["wp_wiki_main_title"]
wp_wiki_main_page_id = conf["wp_wiki_main_page_id"]
wp_wiki_assignments_title = conf["wp_wiki_assignments_title"]
wp_wiki_assignments_page_id = conf["wp_wiki_assignments_page_id"]
wp_wiki_git_manage = conf["wp_wiki_git_manage"]
wp_wiki_git_repo_path = conf["wp_wiki_git_repo_path"]
wp_wiki_ssl = conf["wp_wiki_ssl"]

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    create_input.main()
    main_md = os.path.join(wp_wiki_git_repo_path, "main.md")
    if wp_wiki_ssl:
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://%s/xmlrpc.php" % wp_wiki,
    else:
        url = "http://%s/xmlrpc.php" % wp_wiki,
    if wp_wiki_git_manage:
        if os.path.exists(wp_wiki_git_repo_path):
            try:
                repo = Repo(wp_wiki_git_repo_path)
            except InvalidGitRepositoryError:
                repo = Repo.init(wp_wiki_git_repo_path)
            if repo.git.diff():
                repo.index.add(main_md)
                repo.index.commit(
                    "%s content update" % datetime.now().strftime("%a %b %d %T %Y")
                )
                repo.remotes.origin.push()

    try:
        racks_wiki.update_wiki(
            username=wp_username,
            password=wp_password,
            _page_title=wp_wiki_main_title,
            _page_id=wp_wiki_main_page_id,
            _markdown=main_md,
        )
    except ProtocolError as ex:
        logger.error(ex.errmsg)

    create_input_assignments.main()
    assignments_md = os.path.join(wp_wiki_git_repo_path, "assignments.md")
    if wp_wiki_ssl:
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://%s/xmlrpc.php" % wp_wiki,
    else:
        url = "http://%s/xmlrpc.php" % wp_wiki,

    if wp_wiki_git_manage:
        if os.path.exists(wp_wiki_git_repo_path):
            try:
                repo = Repo(wp_wiki_git_repo_path)
            except InvalidGitRepositoryError:
                repo = Repo.init(wp_wiki_git_repo_path, bare=True)

            if repo.git.diff():
                repo.index.add(assignments_md)
                repo.index.commit(
                    "%s content update" % datetime.now().strftime("%a %b %d %T %Y")
                )
                repo.remotes.origin.push()

    try:
        racks_wiki.update_wiki(
            url="http://%s/xmlrpc.php" % wp_wiki,
            username=wp_username,
            password=wp_password,
            _page_title=wp_wiki_assignments_title,
            _page_id=wp_wiki_assignments_page_id,
            _markdown=assignments_md,
        )
    except ProtocolError as ex:
        logger.error(ex.errmsg)

    regenerate_vlans_wiki()
