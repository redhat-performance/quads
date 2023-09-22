from quads.config import Config
from tests.helpers import unwrap_json


class TestReadVersion:
    def test_valid(self, test_client, auth):
        """
        | GIVEN: Defaults and auth
        | WHEN: User tries to read the current API version
        | THEN: User should be able to get the version
        """
        auth_header = auth.get_auth_header()
        resp = f"QUADS version {Config.QUADSVERSION} {Config.QUADSCODENAME}"
        api_resp = unwrap_json(
            test_client.get(
                "/api/v3/version",
                headers=auth_header,
            )
        )
        assert api_resp.status_code == 200
        assert api_resp.json == resp
