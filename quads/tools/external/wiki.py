#!/usr/bin/python3
import os

from wordpress_xmlrpc import Client, WordPressPage
from wordpress_xmlrpc.methods.posts import EditPost
from urllib.parse import urlparse

import argparse
import ssl


class Wiki:
    def __init__(self, url, username, password):
        """
        Wiki object initialization

        :param url: wordpress url
        :param username: wordpress username
        :param password: wordpress password
        """
        self.url = url
        self.username = username
        self.password = password
        self.endpoint = os.path.join(self.url, "xmlrpc.php")

        scheme = urlparse(self.url)[0]
        if scheme == "https":
            ssl._create_default_https_context = ssl._create_unverified_context

    def update(self, _page_title, _page_id, _markdown):
        """
        Update an existing wordpress page with generated markdown.
        Assumes you have a markdown file with content you want published
        to an existing wordpress page.
        :param _page_title: post page title
        :param _page_id: post page id
        :param _markdown: path to markdown file for upload
        """

        wp = Client(self.endpoint, self.username, self.password)

        # define pages variable
        page = WordPressPage()
        page.title = _page_title

        # page id can be found by viewing via wp-admin dashboard in URL
        page.id = _page_id

        # set local content file to read handle info into a string
        with open(_markdown, "r") as _file:
            page.content = _file.read()

        # post new content to the page
        wp.call(EditPost(page.id, page))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate WordPress WIKI page from Markdown"
    )
    parser.add_argument(
        "--markdown",
        dest="markdown",
        type=str,
        default=None,
        help="Specify markdown input file",
        required=True,
    )
    parser.add_argument(
        "--page-id",
        dest="pageid",
        type=int,
        default=4,
        help="Specify wordpress page id. default = 4",
    )
    parser.add_argument(
        "--wp-url",
        dest="wpurl",
        type=str,
        default=None,
        help="Specify wordpress URL. e.g. http://wiki.example.com",
        required=True,
    )
    parser.add_argument(
        "--wp-username",
        dest="wpusername",
        type=str,
        default=None,
        help="Specify wordpress username.",
        required=True,
    )
    parser.add_argument(
        "--wp-password",
        dest="wppassword",
        type=str,
        default=None,
        help="Specify wordpress password.",
        required=True,
    )
    parser.add_argument(
        "--page-title",
        dest="pagetitle",
        type=str,
        default="Example Wiki Page",
        help="Specify the wiki post title.",
    )

    args = parser.parse_args()

    # authentication and wp url
    wp_url = args.wpurl
    wp_username = args.wpusername
    wp_password = args.wppassword
    markdown = args.markdown
    page_title = args.pagetitle
    page_id = args.pageid

    wiki = Wiki(wp_url, wp_username, wp_password)
    wiki.update(page_title, page_id, markdown)
