"""Client support for network related api calls."""
import json
from hil.client.base import ClientBase
from hil.client.base import check_reserved_chars


class Network(ClientBase):
        """Consists of calls to query and manipulate network related

        objects and relations.
        """

        def list(self):
            """Lists all networks under HIL """
            url = self.object_url('networks')
            return self.check_response(self.httpClient.request("GET", url))

        @check_reserved_chars()
        def list_network_attachments(self, network, project):
            """Lists nodes connected to a network"""
            url = self.object_url('network', network, 'attachments')
            if project == "all":
                return self.check_response(self.httpClient.request("GET", url))

            params = {'project': project}
            return self.check_response(
                    self.httpClient.request("GET", url, params=params))

        @check_reserved_chars()
        def show(self, network):
            """Shows attributes of a network. """
            url = self.object_url('network', network)
            return self.check_response(self.httpClient.request("GET", url))

        @check_reserved_chars(slashes_ok=['net_id'])
        def create(self, network, owner, access, net_id):
            """Create a link-layer <network>.

            See docs/networks.md for details.
            """
            url = self.object_url('network', network)
            payload = json.dumps({
                'owner': owner, 'access': access,
                'net_id': net_id
                })
            return self.check_response(
                    self.httpClient.request("PUT", url, data=payload)
                    )

        @check_reserved_chars()
        def delete(self, network):
            """Delete a <network>. """
            url = self.object_url('network', network)
            return self.check_response(self.httpClient.request("DELETE", url))

        @check_reserved_chars()
        def grant_access(self, project, network):
            """Grants <project> access to <network>. """
            url = self.object_url(
                    'network', network, 'access', project
                    )
            return self.check_response(self.httpClient.request("PUT", url))

        @check_reserved_chars()
        def revoke_access(self, project, network):
            """Removes access of <network> from <project>. """
            url = self.object_url(
                    'network', network, 'access', project
                    )
            return self.check_response(self.httpClient.request("DELETE", url))
