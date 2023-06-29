#!/usr/bin/python3
import logging
import os

from datetime import datetime
from xmlrpc.client import ProtocolError
from git import Repo, InvalidGitRepositoryError
from quads.config import Config
from quads.tools import create_input, create_input_assignments
from quads.tools.external.wiki import Wiki
from quads.tools.regenerate_vlans_wiki import regenerate_vlans_wiki
wp_wiki = Config["wp_wiki"]
wp_username = Config["wp_username"]
wp_password = Config["wp_password"]
wp_wiki_main_title = Config["wp_wiki_main_title"]
wp_wiki_main_page_id = Config["wp_wiki_main_page_id"]
wp_wiki_assignments_title = Config["wp_wiki_assignments_title"]
wp_wiki_assignments_page_id = Config["wp_wiki_assignments_page_id"]
wp_wiki_git_manage = Config["wp_wiki_git_manage"]
wp_wiki_git_repo_path = Config["wp_wiki_git_repo_path"]

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    create_input.main()
    main_md = os.path.join(wp_wiki_git_repo_path, "main.md")
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
        wiki = Wiki(
            url=wp_wiki,
            username=wp_username,
            password=wp_password,
        )
        wiki.update(
            _page_title=wp_wiki_main_title,
            _page_id=wp_wiki_main_page_id,
            _markdown=main_md,
        )
    except ProtocolError as ex:
        logger.error(ex.errmsg)

    create_input_assignments.main()
    assignments_md = os.path.join(wp_wiki_git_repo_path, "assignments.md")
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
        wiki = Wiki(url=wp_wiki, username=wp_username, password=wp_password)
        wiki.update(
            _page_title=wp_wiki_assignments_title,
            _page_id=wp_wiki_assignments_page_id,
            _markdown=assignments_md,
        )
    except ProtocolError as ex:
        logger.error(ex.errmsg)

    regenerate_vlans_wiki()
