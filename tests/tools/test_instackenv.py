#!/usr/bin/env python3
import glob
import os
from datetime import datetime, timedelta

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from quads.tools.make_instackenv_json import main
from tests.cli.config import CLOUD, HOST
from tests.tools.test_base import TestBase


class TestInstackenv(TestBase):
    def setup(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        cloud = CloudDao.create_cloud(CLOUD)
        host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
        vlan = VlanDao.create_vlan(
            "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
        )
        assignment = AssignmentDao.create_assignment(
            "test", "test", "1234", 0, False, [""], vlan.vlan_id, cloud.name
        )
        schedule = ScheduleDao.create_schedule(
            today.strftime("%Y-%m-%d %H:%M"),
            tomorrow.strftime("%Y-%m-%d %H:%M"),
            assignment,
            host,
        )
        assert schedule

    def teardown(self):
        host = HostDao.get_host(HOST)
        cloud = CloudDao.get_cloud(CLOUD)
        schedules = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        if schedules:
            ScheduleDao.remove_schedule(schedules[0].id)
            AssignmentDao.remove_assignment(schedules[0].assignment_id)

        assignments = AssignmentDao.get_assignments()
        for ass in assignments:
            AssignmentDao.remove_assignment(ass.id)

        if host:
            HostDao.remove_host(name=HOST)

        if cloud:
            CloudDao.remove_cloud(CLOUD)

        for f in glob.glob("artifacts/cloud99_*"):
            os.remove(f)

    def test_make_instackenv_json(self):
        Config.__setattr__("openstack_management", True)
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "json_web_path", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        main()
        assert list(
            open(
                os.path.join(
                    os.path.dirname(__file__), "artifacts/cloud99_instackenv.json"
                )
            )
        ) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )

    def test_make_ocpinventory_json(self):
        Config.__setattr__("openshift_management", True)
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "json_web_path", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        main()
        assert list(
            open(
                os.path.join(
                    os.path.dirname(__file__), "artifacts/cloud99_ocpinventory.json"
                )
            )
        ) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )
