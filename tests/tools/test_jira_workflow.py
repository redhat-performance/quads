import asyncio
import unittest
from unittest.mock import patch, AsyncMock

import pytest

from quads.config import Config
from quads.server.dao.cloud import CloudDao
from quads.tools.external.jira import JiraException
from quads.tools.jira_workflow import main


class TestJiraWorkflow(object):

    @patch("quads.tools.external.jira.aiohttp.ClientSession.post")
    @patch("quads.tools.external.jira.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_main(self, mock_get, mock_post):
        resp = AsyncMock()
        resp.json.side_effect = [
            [{"statuses": [{"name": "In Progress", "id": "1"}, {"name": "In Progress", "id": "2"}]}],
            {"issues": [
                {
                    "name": "unitest", "key": "1",
                    "fields": {
                        "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud6\nJustification: Need "
                                       "more time to make unittests",
                        "parent": {
                            "key": "5"
                        },
                        "labels": ["EXTENSION"],
                        "status": "In Progress"
                    },
                },
                {
                    "name": "unitest3", "key": "4",
                    "fields": {
                        "description": "Submitted by: unittest@gmail.com\nCloud to extend: cloud5\nJustification: Need "
                                       "more time to make unittests",
                        "labels": ["EXPANSION"],
                        "status": "In Progress"
                    }
                },
                {
                    "name": "unitest3", "key": "5",
                    "fields": {
                        "description": "Submitted by: unittest@gmail.com\n",
                        "labels": ["EXPANSION"]
                    }
                }
            ]},
            {"transitions": [{"name": "done", "id": "1"}]},
            {"transitions": [{"name": "New", "id": "2"}]},
        ]
        mock_get.return_value.__aenter__.return_value = resp

        post_resp = AsyncMock()
        post_resp.status = 200
        post_resp.json.return_value = {}
        mock_post.return_value.__aenter__.return_value = post_resp

        Config.jira_url = "https://mock_jira.com"
        Config.jira_auth = "token"
        Config.jira_token = "token"
        loop = asyncio.new_event_loop()
        response = await main(_loop=loop)
        assert response == 0

    @patch("quads.tools.external.jira.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_main_error(self, mock_get):
        mock_get.side_effect = JiraException("Jira Exception")
        Config.jira_url = "https://mock_jira.com"
        Config.jira_auth = "basic"
        loop = asyncio.new_event_loop()
        response = await main(_loop=loop)
        assert response == 1
