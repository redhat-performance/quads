"""Client support for extension related api calls."""
from hil.client.base import ClientBase


class Extensions(ClientBase):
    """Consists of calls to query and manipulate extension related

    objects and relations/
    """

    def list_active(self):
        """List all active extensions. """
        url = self.object_url('active_extensions')
        return self.check_response(self.httpClient.request("GET", url))
