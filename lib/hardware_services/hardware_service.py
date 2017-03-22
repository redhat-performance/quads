# EC528 change
#
# This will be an abstract class (perhaps can use abc) that will serve as a generic interface
# for QUADS to interact with its hardware. It will allow QUADS to substitute different hardware
# isolation services while making minimal changes to the current implementation of QUADS.

# This class will declare methods corresponding to the functions defined in lib/libquads.py so that QUADS can
# retain its normal workflow and command options. Once implemented, integration with a new hardware isolation
# service will only require writing a driver that inherits from this class and overwrites its methods with
# its service-specific behavior.

# The hardware service used can be specified at runtime (by changing a single parameter in the conf/quads.yml file).
# A user will specify the name of the service, which will be read in and used as a key in a dictionary (location tbd
# - perhaps in libquads.py, or its own "class mapper" class?) that maps superclass to subclass.
# Duck typing will be used to dynamically assign to a variable in libquads.py a concrete instance of the specified
# subclass (using the "class mapper" dictionary). The quads library will thus be decoupled from any knowledge of
# the specific hardware service being used, as it can now make calls based on this generic interface.
