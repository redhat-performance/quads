import os
from xml.dom import minidom

import requests
import base64
from urllib.parse import urlparse

import argparse
import ssl


class Wordpress:
    def __init__(self, url, username, password):
        """
        Wordpress object initialization

        :param url: wordpress url
        :param username: wordpress username
        :param password: wordpress password
        """
        self.url = url
        self.username = username
        self.password = password
        self.credentials = f"{username}:{password}"
        self.token = base64.b64encode(self.credentials.encode())
        self.header = {"Content-Type": "text/xml;charset=UTF-8"}
        self.api_endpoint = os.path.join(self.url, "xmlrpc.php")
        self.xml_root = minidom.Document()

        scheme = urlparse(self.url)[0]
        if scheme == "https":
            ssl._create_default_https_context = ssl._create_unverified_context

    def create_xml(self, _page_title, _page_id, _markdown):  # pragma: no cover

        # set local content file to read handle info into a string
        with open(_markdown, "r") as _file:
            _content = _file.read()

        methodCall = self.xml_root.createElement("methodCall")
        self.xml_root.appendChild(methodCall)

        methodName = self.xml_root.createElement("methodName")
        methodName.appendChild(self.xml_root.createTextNode("wp.editPost"))
        methodCall.appendChild(methodName)

        params = self.xml_root.createElement("params")

        param_id = self.xml_root.createElement("param")
        param_id_value = self.xml_root.createElement("value")
        param_id_value.appendChild(self.xml_root.createTextNode("1"))
        param_id.appendChild(param_id_value)
        params.appendChild(param_id)

        param_username = self.xml_root.createElement("param")
        param_username_value = self.xml_root.createElement("value")
        param_username_value.appendChild(self.xml_root.createTextNode(str(self.username)))
        param_username.appendChild(param_username_value)
        params.appendChild(param_username)

        param_password = self.xml_root.createElement("param")
        param_password_value = self.xml_root.createElement("value")
        param_password_value.appendChild(self.xml_root.createTextNode(str(self.password)))
        param_password.appendChild(param_password_value)
        params.appendChild(param_password)

        param_post = self.xml_root.createElement("param")
        param_post_value = self.xml_root.createElement("value")
        param_post_value.appendChild(self.xml_root.createTextNode(str(_page_id)))
        param_post.appendChild(param_post_value)
        params.appendChild(param_post)

        # Contents
        param_content = self.xml_root.createElement("param")
        param_content_value = self.xml_root.createElement("value")
        param_content_struct = self.xml_root.createElement("struct")

        # Title
        param_content_member_title = self.xml_root.createElement("member")
        param_content_member_name = self.xml_root.createElement("name")
        param_content_member_name.appendChild(self.xml_root.createTextNode("title"))
        param_content_member_title.appendChild(param_content_member_name)
        param_content_member_name_value = self.xml_root.createElement("value")
        param_content_member_name_value_string = self.xml_root.createElement("string")
        param_content_member_name_value_string.appendChild(self.xml_root.createTextNode(str(_page_title)))
        param_content_member_name_value.appendChild(param_content_member_name_value_string)
        param_content_member_title.appendChild(param_content_member_name_value)
        param_content_struct.appendChild(param_content_member_title)

        # Post content
        param_content_member_content = self.xml_root.createElement("member")
        param_content_member_content_name = self.xml_root.createElement("name")
        param_content_member_content_name.appendChild(self.xml_root.createTextNode("post_content"))
        param_content_member_content.appendChild(param_content_member_content_name)
        param_content_member_content_value = self.xml_root.createElement("value")
        param_content_member_content_value_string = self.xml_root.createElement("string")
        param_content_member_content_value_string.appendChild(self.xml_root.createTextNode(str(_content)))
        param_content_member_content_value.appendChild(param_content_member_content_value_string)
        param_content_member_content.appendChild(param_content_member_content_value)
        param_content_struct.appendChild(param_content_member_content)

        # Post excerpt
        param_content_member_excerpt = self.xml_root.createElement("member")
        param_content_member_excerpt_name = self.xml_root.createElement("name")
        param_content_member_excerpt_name.appendChild(self.xml_root.createTextNode("excerpt"))
        param_content_member_excerpt.appendChild(param_content_member_excerpt_name)
        param_content_member_excerpt_value = self.xml_root.createElement("value")
        param_content_member_excerpt_value_string = self.xml_root.createElement("string")
        param_content_member_excerpt_value_string.appendChild(self.xml_root.createTextNode(""))
        param_content_member_excerpt_value.appendChild(param_content_member_excerpt_value_string)
        param_content_member_excerpt.appendChild(param_content_member_excerpt_value)
        param_content_struct.appendChild(param_content_member_excerpt)

        # Append contents
        param_content_value.appendChild(param_content_struct)
        param_content.appendChild(param_content_value)
        params.appendChild(param_content)
        methodCall.appendChild(params)

        return self.xml_root.toxml()

    def update_page(self, _page_title, _page_id, _markdown):  # pragma: no cover
        """
        Update an existing wordpress page with generated markdown.
        Assumes you have a markdown file with content you want published
        to an existing wordpress page.
        :param _page_title: post page title
        :param _page_id: post page id
        :param _markdown: path to markdown file for upload
        """
        payload = self.create_xml(_page_title, _page_id, _markdown)
        response = requests.post(self.api_endpoint, headers=self.header, data=payload.encode(encoding="utf-8"))

        if response.status_code == 200:
            print(f"Successfully updated {_page_title} page.")


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Generate WordPress WIKI page from Markdown")
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

    wiki = Wordpress(wp_url, wp_username, wp_password)
    wiki.update_page(page_title, page_id, markdown)
