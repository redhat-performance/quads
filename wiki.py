#!/usr/bin/env python
# Update an existing wiki page with generated markdown

from wordpress_xmlrpc import WordPressPage
import os

#authentication
wp_url = "http://wiki.example.com/xmlrpc.php"
wp_username = "admin"
wp_password = "admin"
wp = Client(wp_url, wp_username, wp_password)

# define pages variable
pages = client.call(posts.GetPosts({'post_type': 'page'}, results_class=WordPressPage))
page = WordPressPage()
page.title = 'Example Scale Data Post'
# page id can be found by viewing via wp-admin dashboard in URL
page.id = '9'

# pull page from generated/converted markdown
page.content = open('/tmp/update-page.md', 'r')
wp.call(posts.EditPost(page.id, page))
