"""Regression tests for user date handling (issue #681).

The login flow sends ``last_login`` as an ISO string
(``auth_helpers.py`` uses ``datetime.now().isoformat()``).  The DAO used to
assign that raw string to the DateTime column, which SQLAlchemy rejects
(``SQLite DateTime type only accepts Python datetime and date objects as
input``).  It must be normalized through ``parse_datetime`` first, matching
the convention ``Serialize.from_dict`` already uses for every other model.
"""

from datetime import datetime

import pytest

from quads.server.dao.user import UserDao
from tests.helpers import unwrap_json


@pytest.mark.parametrize(
    "raw, expected",
    [
        # naive ISO, exactly what datetime.now().isoformat() produces
        ("2026-09-08T14:37:00.123456", datetime(2026, 9, 8, 14, 37, 0, 123456)),
    ],
)
def test_update_user_normalizes_datetime_string(test_client, raw, expected):
    user = UserDao.update_user("gonza@redhat.com", last_login=raw)
    assert isinstance(user.last_login, datetime)
    assert user.last_login == expected


def test_update_user_last_login_api_returns_gmt(test_client, auth):
    headers = auth.get_auth_header()
    # Create a user in the configured domain (example.com) so is_valid_domain
    # passes, then PATCH its last_login.
    create = unwrap_json(
        test_client.post(
            "/api/v3/users/",
            json={"email": "login_user@example.com"},
        )
    )
    assert create.status_code == 201
    response = unwrap_json(
        test_client.patch(
            "/api/v3/users/login_user@example.com",
            json={"last_login": "2026-09-08T14:37:00.123456"},
            headers=headers,
        )
    )
    assert response.status_code == 200
    assert response.json["last_login"] is not None
    assert response.json["last_login"].endswith("GMT")
