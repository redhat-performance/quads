# EC528 change
#
# This will be an abstract class (perhaps can use abc) that will serve as a generic interface
# for QUADS to interact with and isolate its hardware. It will allow QUADS to substitute different hardware
# isolation services while making minimal changes to the current implementation of QUADS.
#
# This class will declare methods corresponding to the functions defined in lib/libquads.py so that QUADS can
# retain its normal workflow and command options. Once implemented, integration with a new hardware isolation
# service will only require writing a driver that inherits from this class and overwrites its methods with
# its service-specific behavior.
#
# The hardware service used can be specified at runtime (by changing a single parameter in the conf/quads.yml file).
# A user will specify the name of the service, which will be read in and used as a key in a dictionary (location tbd
# - perhaps in libquads.py, or its own "class mapper" class?) that maps superclass to subclass.
# Duck typing will be used to dynamically assign to a variable in libquads.py a concrete instance of the specified
# subclass (using the "class mapper" dictionary). The quads library will thus be decoupled from any knowledge of
# the specific hardware service being used, as it can now make calls based on this generic interface.
#
#
# abstract methods to be overwritten by concrete subclasses:
# note: these are only examples and do not describe the actual prototypes
#
#   remove_host():
#   remove_cloud():
#   update_host():
#   update_cloud():
#   move_hosts():
#   list_hosts():
#   list_clouds():
#
# this list may need to expand to accommodate for scheduling behavior, but for now we assume that scheduling
# will be able to continue with minimal changes (only thing that this will change is where QUADS pulls its data from)
#####################################################################################################################

import sys
from abc import ABCMeta, abstractmethod

class HardwareService(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def update_cloud(self, **kwargs):
        """ TODO add documentation
        """

    @abstractmethod
    def update_host(self, **kwargs):
        """ TODO add documentation
        """

    @abstractmethod
    def remove_cloud(self, **kwargs):
        """ TODO add documentation
        """

    @abstractmethod
    def remove_host(self, **kwargs):
        """ TODO add documentation
        """

    @abstractmethod
    def move_hosts(self, **kwargs):
        """ TODO add documentation
        """

    @abstractmethod
    def list_clouds(self):
        """ TODO add documentation
        """

    @abstractmethod
    def list_hosts(self):
        """ TODO add documentation
        """


_hardware_service = None


def set_hardware_service(hardware_service):

    global _hardware_service
    if _hardware_service is not None:
        sys.exit("Error: _hardware_service already set")

    _hardware_service = hardware_service


def get_hardware_service():
    return _hardware_service



