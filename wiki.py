#!/usr/bin/env python
# Update an existing wiki page with generated markdown
# requires: python-wordpress-xmlrpc

from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods.taxonomies import *
from wordpress_xmlrpc.methods.posts import *
from wordpress_xmlrpc.methods.users import *
from wordpress_xmlrpc.methods import *

#authentication
wp_url = "http://wiki.example.com/xmlrpc.php"
wp_username = "admin"
wp_password = "admin"
wp = Client(wp_url, wp_username, wp_password)

# define pages variable
page = WordPressPage()
page.title = 'Example Scale Data Post'
# page id can be found by viewing via wp-admin dashboard in URL
page.id = 9
# pull page from generated/converted markdown
# set local file to read handle from
f = open('/tmp/update-page.md', 'r')
page.content = f.read()
wp.call(EditPost(page.id, page))
