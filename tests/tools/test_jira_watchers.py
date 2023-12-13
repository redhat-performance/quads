import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

import pytest

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from quads.tools.external.jira import JiraException
from quads.tools.jira_watchers import main


@patch("quads.tools.external.postman.SMTP")
@patch("quads.tools.external.jira.aiohttp.ClientSession.put")
@patch("quads.tools.external.jira.aiohttp.ClientSession.post")
@patch("quads.tools.external.jira.aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_main(mock_get, mock_post, mock_put, mock_smtp):
    today = datetime.now()
    tomorrow = today + timedelta(weeks=2)

    CloudDao.create_cloud("cloud1")
    HostDao.create_host("host.example.com", "r640", "unittest", "cloud1")
    host = HostDao.get_host("host.example.com")
    cloud = CloudDao.get_cloud("cloud1")
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    assignment = AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)
    ScheduleDao.create_schedule(today.strftime("%Y-%m-%d %H:%M"), tomorrow.strftime("%Y-%m-%d %H:%M"),
                                assignment, host)
    resp = AsyncMock()
    resp.json.side_effect = [
        {"issues": [
            {
                "name": "unitest", "key": "1",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud1\nJustification: Need "
                                   "more time to make unittests",
                    "parent": {
                        "key": "5"
                    },
                    "labels": ["EXTENSION"]}
            },
            {
                "name": "unitest3", "key": "4",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud2\nJustification: Need "
                                   "more time to make unittests",
                    "labels": ["EXPANSION"]
                }
            },
            {
                "name": "unitest3", "key": "4",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\n",
                    "labels": ["EXPANSION"]
                }
            }
        ]},
        {"issues": [{"statusCategory": 4, "name": "unitest", "key": "2"}]},
        {"watchers": [{"key": "1"}]},
    ]
    mock_get.return_value.__aenter__.return_value = resp

    post_resp = AsyncMock()
    post_resp.status = 200
    post_resp.json.return_value = {}
    mock_post.return_value.__aenter__.return_value = post_resp

    put_resp = AsyncMock()
    put_resp.status = 200
    put_resp.json.return_value = {}
    mock_put.return_value.__aenter__.return_value = put_resp

    Config.jira_url = "https://mock_jira.com"
    Config.jira_auth = "token"
    Config.jira_token = "token"
    loop = asyncio.new_event_loop()
    response = await main(_loop=loop)
    assert response == 0
    CloudDao.remove_cloud("cloud1")
    HostDao.remove_host("host.example.com")
    AssignmentDao.remove_assignment(assignment_id=assignment.id)


@patch("quads.tools.external.postman.SMTP")
@patch("quads.tools.external.jira.aiohttp.ClientSession.put")
@patch("quads.tools.external.jira.aiohttp.ClientSession.post")
@patch("quads.tools.external.jira.aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_main_post_fail(mock_get, mock_post, mock_put, mock_smtp):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    CloudDao.create_cloud("cloud6")
    HostDao.create_host("host5.example.com", "r640", "unittest", "cloud6")
    host = HostDao.get_host("host5.example.com")
    cloud = CloudDao.get_cloud("cloud6")
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    assignment = AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)
    ScheduleDao.create_schedule(today.strftime("%Y-%m-%d %H:%M"), tomorrow.strftime("%Y-%m-%d %H:%M"),
                                assignment, host)
    resp = AsyncMock()
    resp.json.side_effect = [
        {"issues": [
            {
                "name": "unitest", "key": "1",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud6\nJustification: Need "
                                   "more time to make unittests",
                    "parent": {
                        "key": "5"
                    },
                    "labels": ["EXTENSION"]}
            },
            {
                "name": "unitest3", "key": "4",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud5\nJustification: Need "
                                   "more time to make unittests",
                    "labels": ["EXPANSION"]
                }
            },
            {
                "name": "unitest3", "key": "4",
                "fields": {
                    "description": "Submitted by: unittest@gmail.com\n",
                    "labels": ["EXPANSION"]
                }
            }
        ]},
        {"issues": [{"statusCategory": 4, "name": "unitest", "key": "2"}]},
        {"watchers": [{"key": "1"}]},
    ]
    mock_get.return_value.__aenter__.return_value = resp

    post_resp = AsyncMock()
    post_resp.status = 404
    post_resp.json.return_value = {}
    mock_post.return_value.__aenter__.return_value = post_resp

    put_resp = AsyncMock()
    put_resp.status = 404
    put_resp.json.return_value = {}
    mock_put.return_value.__aenter__.return_value = put_resp

    Config.jira_url = "https://mock_jira.com"
    Config.jira_auth = "token"
    Config.jira_token = "token"
    loop = asyncio.new_event_loop()
    response = await main(_loop=loop)
    assert response == 0


@patch("quads.tools.external.jira.aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_main_empty(mock_get):
    resp = AsyncMock()
    resp.json.side_effect = [
        {"issues": []},
        {"issues": []}
    ]
    mock_get.return_value.__aenter__.return_value = resp
    Config.jira_url = "https://mock_jira.com"
    Config.jira_auth = "token"
    Config.jira_token = "token"
    loop = asyncio.new_event_loop()
    response = await main(_loop=loop)
    assert response == 0


@patch("quads.tools.external.jira.aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_main_error(mock_get):
    mock_get.side_effect = JiraException("Jira Exception")
    Config.jira_url = "https://mock_jira.com"
    Config.jira_auth = "basic"
    loop = asyncio.new_event_loop()
    response = await main(_loop=loop)
    assert response == 1
