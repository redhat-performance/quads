"""Client library for user-oriented api calls.

These are only meaningful if the server is configured to use
username & password auth.
"""
import json
from hil.client.base import ClientBase
from hil.client.base import check_reserved_chars


class User(ClientBase):
    """Consists of calls to query and

    manipulate users related objects and relations.
    """
    def list(self):
        """List all users"""
        url = self.object_url('/auth/basic/users')
        return self.check_response(self.httpClient.request("GET", url))

    @check_reserved_chars(dont_check=['password', 'is_admin'])
    def create(self, username, password, is_admin):
        """Create a user <username> with password <password>.

        <is_admin> is a boolean,
        and determines whether a user is authorized for
        administrative privileges.
        """
        url = self.object_url('/auth/basic/user', username)

        payload = json.dumps({
                'password': password, 'is_admin': is_admin,
                })
        return self.check_response(
                self.httpClient.request("PUT", url, data=payload)
                )

    @check_reserved_chars()
    def delete(self, username):
        """Deletes the user <username>. """
        url = self.object_url('/auth/basic/user', username)
        return self.check_response(
                self.httpClient.request("DELETE", url)
                )

    @check_reserved_chars()
    def add(self, user, project):
        """Adds <user> to a <project>. """
        url = self.object_url('/auth/basic/user', user, 'add_project')
        payload = json.dumps({'project': project})
        return self.check_response(
                self.httpClient.request("POST", url, data=payload)
                )

    @check_reserved_chars()
    def remove(self, user, project):
        """Removes all access of <user> to <project>. """
        url = self.object_url('/auth/basic/user', user, 'remove_project')
        payload = json.dumps({'project': project})
        return self.check_response(
                self.httpClient.request("POST", url, data=payload)
                )

    @check_reserved_chars(dont_check=['is_admin'])
    def set_admin(self, username, is_admin):
        """Changes the admin status of <username>.

        <is_admin> is a boolean that determines
        whether a user is authorized for
        administrative privileges.
        """

        url = self.object_url('/auth/basic/user', username)
        payload = json.dumps({'is_admin': is_admin})
        return self.check_response(
                self.httpClient.request("PATCH", url, data=payload)
                )
