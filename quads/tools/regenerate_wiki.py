#!/usr/bin/env python

import os
from datetime import datetime
from git import Repo, InvalidGitRepositoryError
from quads.config import conf
from quads.tools import create_input, create_input_assignments, racks_wiki


wp_wiki = conf["wp_wiki"]
wp_username = conf["wp_username"]
wp_password = conf["wp_password"]
wp_wiki_main_title = conf["wp_wiki_main_title"]
wp_wiki_main_page_id = conf["wp_wiki_main_page_id"]
wp_wiki_assignments_title = conf["wp_wiki_assignments_title"]
wp_wiki_assignments_page_id = conf["wp_wiki_assignments_page_id"]
wp_wiki_git_manage = conf["wp_wiki_git_manage"]
wp_wiki_git_repo_path = conf["wp_wiki_git_repo_path"]

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
                repo.index.commit("%s content update" % datetime.now().strftime("%a %b %d %T %Y"))
                repo.remotes.origin.push()

    racks_wiki.update_wiki(
        url="http://%s/xmlrpc.php" % wp_wiki,
        username=wp_username,
        password=wp_password,
        _page_title=wp_wiki_main_title,
        _page_id=wp_wiki_main_page_id,
        _markdown=main_md,
    )

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
                repo.index.commit("%s content update" % datetime.now().strftime("%a %b %d %T %Y"))
                repo.remotes.origin.push()

    racks_wiki.update_wiki(
        url="http://%s/xmlrpc.php" % wp_wiki,
        username=wp_username,
        password=wp_password,
        _page_title=wp_wiki_assignments_title,
        _page_id=wp_wiki_assignments_page_id,
        _markdown=assignments_md,
    )
