#!/usr/bin/env python
# Update an existing wordpress page with generated markdown
# Assumes you have a markdown file with content you want published
# to an existing wordpress page.
# requires: python-wordpress-xmlrpc or python3-wordpress-xmlrpc

from wordpress_xmlrpc import Client, WordPressPage
from wordpress_xmlrpc.methods.posts import EditPost
import argparse


def update_page(wp_url, wp_username, wp_password, markdown, page_title, page_id):
    wp = Client(wp_url, wp_username, wp_password)

    # define pages variable
    page = WordPressPage()
    page.title = page_title

    # page id can be found by viewing via wp-admin dashboard in URL
    page.id = page_id

    # set local content file to read handle info into a string
    with open(markdown, 'r') as f:
        page.content = f.read()

    # post new content to the page
    wp.call(EditPost(page.id, page))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate WordPress WIKI page from Markdown')
    parser.add_argument('--markdown', dest='markdown', type=str, default=None, help='Specify markdown input file')
    parser.add_argument('--page-id', dest='pageid', type=int, default=4, help='Specify wordpress page id. default = 4')
    parser.add_argument('--wp-url', dest='wpurl', type=str, default=None, help='Specify wordpress URL. e.g. http://wiki.example.com/xmlrpc.php')
    parser.add_argument('--wp-username', dest='wpusername', type=str, default=None, help='Specify wordpress username.')
    parser.add_argument('--wp-password', dest='wppassword', type=str, default=None, help='Specify wordpress password.')
    parser.add_argument('--page-title', dest='pagetitle', type=str, default=None, help='Specify the wiki post title.')

    args=parser.parse_args()

    # authentication and wp url
    _wp_url = args.wpurl
    _wp_username = args.wpusername
    _wp_password = args.wppassword
    _markdown = args.markdown
    _page_title = args.pagetitle
    _page_id = args.pageid

    def missing_arg(parameter):
        print "Required parameter missing: " + parameter
        exit(1)

    if _wp_url is None:
        missing_arg('--wp-url')

    if _wp_username is None:
        missing_arg('--wp-username')

    if _wp_password is None:
        missing_arg('--wp-password')

    if _markdown is None:
        missing_arg('--markdown')

    if _page_title is None:
        _page_title = 'Example Wiki Page'

    update_page(_wp_url, _wp_username, _wp_password, _markdown, _page_title, _page_id)
