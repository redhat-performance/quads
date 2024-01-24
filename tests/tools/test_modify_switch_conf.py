import pytest

from quads.quads_api import APIBadRequest
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.tools.modify_switch_conf import verify as modify_switch_verify


def test_verify_false():
    with pytest.raises(APIBadRequest):
        modify_switch_verify("host.verify.example.com.example.com")


def test_verify_empty():
    CloudDao.create_cloud("cloudverify")
    HostDao.create_host("host.verify.example.com", "r640", "unittest", "cloudverify")
    response = modify_switch_verify("host.verify.example.com")
    assert not response
    HostDao.remove_host("host.verify.example.com")
    CloudDao.remove_cloud("cloudverify")
