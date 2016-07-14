#!/usr/bin/env python
# Update an existing wiki page with generated markdown
# requires: python-wordpress-xmlrpc

from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods.taxonomies import *
from wordpress_xmlrpc.methods.posts import *
from wordpress_xmlrpc.methods.users import *
from wordpress_xmlrpc.methods import *

#authentication
wp_url = "http://wiki.example/xmlrpc.php"
wp_username = "admin"
wp_password = "admin"
wp = Client(wp_url, wp_username, wp_password)

# define pages variable
page = WordPressPage()
page.title = 'Example Scale Data Post'
# page id can be found by viewing via wp-admin dashboard in URL
page.id = 9
# pull page from generated/converted markdown
# FIXME: probably need a markdown or similiar lib here
# as it doesn't like page.content with open('file', 'r')
page.content = open('/tmp/update-page.md', 'r')
# post page update
wp.call(EditPost(page.id, page))
