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

# authentication and wp url
wp_url = "http://wiki.example.com/xmlrpc.php"
wp_username = "admin"
wp_password = "admin"
wp = Client(wp_url, wp_username, wp_password)

# define pages variable
page = WordPressPage()
page.title = 'RDU Scale Lab Racks'

# page id can be found by viewing via wp-admin dashboard in URL
page.id = 4

# set local content file to read handle info into a string
f = open('update-racks-page.md', 'r')
page.content = f.read()

# post new content to the page
wp.call(EditPost(page.id, page))
