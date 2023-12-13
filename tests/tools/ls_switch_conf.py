
from quads.tools.ls_switch_conf import verify


def test_verify_ls_switch_conf_not_present():
    assert not verify("cloud0")

