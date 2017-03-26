#!/bin/python
import sys
from hardware_services.hardware_service import get_hardware_service, set_hardware_service
from hardware_services.hardware_drivers.mock_driver import MockDriver

set_hardware_service(MockDriver())

cls = get_hardware_service()

cls.update_cloud()
cls.update_host()
cls.remove_cloud()
cls.remove_host()
cls.move_hosts()
cls.list_clouds()
cls.list_hosts()

