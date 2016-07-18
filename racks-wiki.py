#!/usr/bin/env python
# Update an existing wordpress page with generated markdown
# Assumes you have a markdown file with content you want published
# to an existing wordpress page.
# requires: python2-wordpress-xmlrpc or python3-wordpress-xmlrpc

from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods.taxonomies import *
from wordpress_xmlrpc.methods.posts import *
from wordpress_xmlrpc.methods.users import *
from wordpress_xmlrpc.methods import *
from subprocess import call
import argparse
import os

parser = argparse.ArgumentParser(description='Generate WordPress WIKI page from Markdown')
parser.add_argument('--markdown', dest='markdown', type=str, default=None, help='Specify markdown input file')
parser.add_argument('--page-id', dest='pageid', type=int, default=4, help='Specify wordpress page id. default = 4')
parser.add_argument('--wp-url', dest='wpurl', type=str, default=None, help='Specify wordpress URL. e.g. http://wiki.example.com/xmlrpc.php')
parser.add_argument('--wp-username', dest='wpusername', type=str, default=None, help='Specify wordpress username.')
parser.add_argument('--wp-password', dest='wppassword', type=str, default=None, help='Specify wordpress password.')
parser.add_argument('--page-title', dest='pagetitle', type=str, default=None, help='Specify the wiki post title.')

args=parser.parse_args()

# authentication and wp url
wp_url = args.wpurl
wp_username = args.wpusername
wp_password = args.wppassword
markdown = args.markdown
pagetitle = args.pagetitle

def missing_arg(parameter):
    print "Required parameter missing: " + parameter
    exit(1)

if wp_url is None:
    missing_arg('--wp-url')

if wp_username is None:
    missing_arg('--wp-username')

if wp_password is None:
    missing_arg('--wp-password')

if markdown is None:
    missing_arg('--markdown')

if pagetitle is None:
    pagetitle = 'Example Wiki Page'
    
wp = Client(wp_url, wp_username, wp_password)

# define pages variable
page = WordPressPage()
page.title = pagetitle

# page id can be found by viewing via wp-admin dashboard in URL
page.id = args.pageid

# set local content file to read handle info into a string
f = open(markdown, 'r')
page.content = f.read()

# post new content to the page
wp.call(EditPost(page.id, page))
