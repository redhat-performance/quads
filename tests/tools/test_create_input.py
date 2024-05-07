import os.path
import pathlib
import tempfile
from unittest.mock import AsyncMock, Mock, patch

import pytest

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.vlan import VlanDao
from quads.tools.create_input import (
    render_header,
    render_row,
    main as create_input_main,
    rack_has_hosts,
)
from tests.cli.config import HOST1, IFMAC1, CLOUD
from tests.tools.config import HOST_E20, HOST_C02, HOST_C08, HOST_C01


class TestCreateInput(object):
    def test_render_header(self):
        response = render_header("unittest")
        assert "unittest" in response.lower()

    def test_render_row(self):
        cloud_name = CLOUD
        host_name = HOST_E20
        _host_obj = HostDao.get_host(host_name)
        _properties = {
            "svctag": "test",
            "host_mac": IFMAC1,
            "host_ip": "10.20.48.0",
            "ip": "10.20.48.0",
            "mac": IFMAC1,
        }
        cloud = CloudDao.get_cloud(cloud_name)
        vlan = VlanDao.create_vlan(
            "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
        )
        assignment = AssignmentDao.create_assignment(
            "test", "unittest", "1234", 0, False, [""], cloud.name, vlan.vlan_id
        )
        response = render_row(_host_obj, _properties)
        assert (
            "<a href=http://mgmt-e20-h17-6029p.example.com/ target=_blank>console</a>"
            in response
        )
        assert "e20-h17-6029p" in response
        AssignmentDao.delete_assignment(assignment.id)
        HostDao.remove_host(host_name)
        CloudDao.remove_cloud(cloud_name)

    def test_rack_has_hosts(self):
        assert not rack_has_hosts(Config["racks"], {})

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    def test_create_input_main(self, mock_get):
        cloud_name = CLOUD
        host_name = HOST_C02
        HostDao.create_host(host_name, "r640", "unittest-user", cloud_name)
        _host_obj = HostDao.get_host(host_name)
        cloud = CloudDao.get_cloud(cloud_name)
        vlan = VlanDao.create_vlan(
            "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
        )
        assignment = AssignmentDao.create_assignment(
            "test", "unittest", "1234", 0, False, [""], cloud.name, vlan.vlan_id
        )
        resp = AsyncMock()
        resp.json.return_value = {
            "results": [
                {
                    "name": host_name,
                    "sp_name": True,
                    "ip": "10.19.96.56",
                    "sp_ip": "10.19.96.57",
                    "mac": "24:6e:96:bd:d4:6a",
                    "sp_mac": "d0:94:66:64:54:f4",
                },
                {
                    "name": HOST_C08,
                    "ip": "10.19.96.56",
                    "sp_ip": "10.19.96.57",
                    "mac": "24:6e:96:bd:d4:6a",
                    "sp_mac": "d0:94:66:64:54:f4",
                },
                {
                    "name": HOST_C01,
                    "ip": "10.19.96.56",
                    "sp_ip": "10.19.96.57",
                    "mac": "24:6e:96:bd:d4:6a",
                    "sp_mac": "d0:94:66:64:54:f4",
                },
            ]
        }
        mock_get.return_value.__aenter__.return_value = resp
        with tempfile.TemporaryDirectory() as tmp_dirname:
            Config.__setattr__("data_dir", tmp_dirname)
            wp_wiki_git_repo_path = os.path.join(tmp_dirname, "test")
            Config.__setattr__("wp_wiki_git_repo_path", wp_wiki_git_repo_path)
            create_input_main()
            assert os.path.exists(os.path.join(wp_wiki_git_repo_path, "main.md"))
        AssignmentDao.delete_assignment(assignment.id)
        HostDao.remove_host(host_name)
        CloudDao.remove_cloud(cloud_name)

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    def test_create_input_main_empty_hosts(self, mock_get):
        resp = AsyncMock()
        resp.json.return_value = {"results": []}
        mock_get.return_value.__aenter__.return_value = resp
        with tempfile.TemporaryDirectory() as tmp_dirname:
            Config.__setattr__("data_dir", tmp_dirname)
            Config.__setattr__("wp_wiki_git_repo_path", tmp_dirname)
            pathlib.Path(tmp_dirname).mkdir(parents=True, exist_ok=True)
            assert not os.path.exists(os.path.join(tmp_dirname, "main.md"))
            create_input_main()
            assert os.path.exists(os.path.join(tmp_dirname, "main.md"))

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    def test_create_input_main_svctag(self, mock_get):
        host_name = HOST_E20
        resp = AsyncMock()
        resp.json.return_value = {
            "results": [
                {
                    "name": host_name,
                    "sp_name": True,
                    "ip": "10.19.96.58",
                    "sp_ip": "10.19.96.59",
                    "mac": "24:6e:96:bd:d4:6b",
                    "sp_mac": "d0:94:66:64:54:f5",
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = resp
        with tempfile.TemporaryDirectory() as tmp_dirname:
            Config.__setattr__("data_dir", tmp_dirname)
            Config.__setattr__("wp_wiki_git_repo_path", tmp_dirname)
            pathlib.Path(tmp_dirname).mkdir(parents=True, exist_ok=True)
            svctag_path = os.path.join(tmp_dirname, "ipmi", host_name)
            pathlib.Path(svctag_path).mkdir(parents=True, exist_ok=True)
            svctag_file = os.path.join(svctag_path, "svctag")
            with open(svctag_file, "w") as svctag:
                svctag.write("unittest")
            assert not os.path.exists(os.path.join(tmp_dirname, "main.md"))
            create_input_main()
            assert os.path.exists(os.path.join(tmp_dirname, "main.md"))
