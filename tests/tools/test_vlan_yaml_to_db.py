import os
import tempfile

import pytest

from quads.tools.vlan_yaml_to_db import main as vlan_yaml_to_db_main


def test_vlan_yaml_main_empty():
    class Args:
        yaml = ""
    args = Args()
    vlan_yaml_to_db_main(args)
    assert not args.yaml


def test_vlan_yaml_main_path_not_exists():
    class Args:
        yaml = "/tmp/unittest.yml"
    args = Args()
    with pytest.raises(SystemExit) as exit:
        vlan_yaml_to_db_main(args)
    assert int(str(exit.value)) == 1


def test_vlan_yaml_main():

    class Args:
        yaml = os.path.join(os.path.dirname(__file__), "../../conf/vlans.yml")
    args = Args()
    vlan_yaml_to_db_main(args)
    vlan_yaml_to_db_main(args)


def test_vlan_yaml_main_no_contents():
    with tempfile.NamedTemporaryFile(suffix=".yml") as temp_file:
        temp_filepath = temp_file.name
        class Args:
            yaml = temp_filepath
        args = Args()
        vlan_yaml_to_db_main(args)
        assert os.path.getsize(temp_filepath) == 0


def test_vlan_yaml_main_yaml_error():

    class Args:
        yaml = "./test_yaml_errors.yml"
    args = Args()
    with pytest.raises(SystemExit) as exit:
        vlan_yaml_to_db_main(args)
    assert int(str(exit.value)) == 1
