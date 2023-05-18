import pytest
import base64

from quads.database import init_db
from tests.helpers import unwrap_json
from quads.server.app import (
    create_app,
    db_init,
    populate,
    user_datastore,
    drop_all,
)
from tests.config import *


@pytest.fixture(scope="module")
def test_client():
    """
    | Creates a test client for the app from the testing config.
    | Drops and then initializes the database and populates it with default users.
    """
    flask_app = create_app()
    flask_app.config.from_object("quads.server.config.TestingConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            drop_all(flask_app.config)
            init_db()
            populate(user_datastore)
            yield testing_client


class AuthActions(object):
    """
    | Helper class for authentication actions.
    | Used through the auth fixture.
    | Only `get_auth_header()` should be used in tests.
    """

    def __init__(self, client):
        self._client = client
        self._token = None
        self._username = ""

    def login(self, username="grafuls@redhat.com", password="password"):
        valid_credentials = base64.b64encode(
            f"{username}:{password}".encode("utf-8")
        ).decode("utf-8")
        response = unwrap_json(
            self._client.post(
                "/api/v3/login",
                json=dict(),
                headers={"Authorization": "Basic " + valid_credentials},
            )
        )
        self._token = response.json["auth_token"]
        self._username = username

    def logout(self):
        self._client.post(
            "/api/v3/logout",
            json=dict(),
            headers=self.get_auth_header(),
        )
        self._token = None
        self._username = ""

    def get_auth_header(self, username="grafuls@redhat.com", password="password"):
        if self._token is None and self._username == "":
            self.login(username, password)
        if self._username != username:
            self.logout()
            self.login(username, password)
        return {"Authorization": f"Bearer {self._token}"}


@pytest.fixture(scope="module")
def auth(test_client):
    """Fixture to access authentication actions in `AuthActions`."""
    return AuthActions(test_client)


@pytest.fixture(scope="module")
def prefill(test_client, auth, request):
    """Fixture to prefill the database with data.

    With `request.param`, list with first argument being a string, with all the specified options of what to prefill.
    Parameters can be specified with `pytest.mark.parametrize()`.

    | Supported parameters for `request.param`:
    |    clouds - prefill with clouds
    |    vlans - prefill with vlans
    |    hosts - prefill with hosts (requires clouds)
    |    disks - prefill with disks (requires clouds and hosts)
    |    interfaces - prefill with interfaces (requires clouds and hosts)
    |    memory - prefill with memory (requires clouds and hosts)
    |    processors - prefill with processors (requires clouds and hosts)
    |    assignments - prefill with assignments (requires clouds and vlans)
    |    schedules - prefill with schedules (requires clouds, hosts, vlans, and assignments)

    Example:
        >>> # prefill with clouds, hosts and disks
        >>> @pytest.mark.parametrize("prefill", ["clouds, hosts, disks"], indirect=True)
        >>> def test_name(self, test_client, auth, prefill):
        >>>     do_something()
        >>>     assert some_result == something
    """

    auth_header = auth.get_auth_header()
    if "clouds" in request.param:
        for cloud_id in range(1, 6):
            cloud_name = f"cloud{str(cloud_id).zfill(2)}"
            test_client.post(
                "/api/v3/clouds",
                json=dict(name=cloud_name),
                headers=auth_header,
            )
    if "vlans" in request.param:
        for i in range(1, 4):
            test_client.post(
                f"/api/v3/vlans",
                json=eval(f"VLAN_{i}_REQUEST"),
                headers=auth_header,
            )
    if "hosts" in request.param:
        for host_id in range(1, 6):
            test_client.post(
                "/api/v3/hosts",
                json=eval(f"HOST_{host_id}_REQUEST"),
                headers=auth_header,
            )
    if "disks" in request.param:
        for i in range(1, 5):
            disk_request = eval(f"DISK_{i}_REQUEST")
            test_client.post(
                f"/api/v3/disks/{disk_request[1]}",
                json=disk_request[0],
                headers=auth_header,
            )
    if "interfaces" in request.param:
        _ = INTERFACE_1_REQUEST
        for i in range(1, 5):
            interface_request = eval(f"INTERFACE_{i}_REQUEST")
            test_client.post(
                f"/api/v3/interfaces/{interface_request[1]}",
                json=interface_request[0],
                headers=auth_header,
            )
    if "memory" in request.param:
        for i in range(1, 7):
            memory_request = eval(f"MEMORY_{i}_REQUEST")
            test_client.post(
                f"/api/v3/memory/{memory_request[1]}",
                json=memory_request[0],
                headers=auth_header,
            )
    if "processors" in request.param:
        for i in range(1, 6):
            processor_request = eval(f"PROCESSOR_{i}_REQUEST")
            test_client.post(
                f"/api/v3/processors/{processor_request[1]}",
                json=processor_request[0],
                headers=auth_header,
            )
    if "assignments" in request.param:
        for i in range(1, 3):
            assignment_request = eval(f"ASSIGNMENT_{i}_REQUEST")
            test_client.post(
                f"/api/v3/assignments",
                json=assignment_request,
                headers=auth_header,
            )
    if "schedules" in request.param:
        for i in range(1, 3):
            schedule_request = eval(f"SCHEDULE_{i}_REQUEST")
            test_client.post(
                f"/api/v3/schedules",
                json=schedule_request,
                headers=auth_header,
            )
