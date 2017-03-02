Provisioning Templates
======================

This includes snippets, templates and provisioning system-specific files.

* Right now this just contains Foreman snippets we might use or host parameters we depend upon for certain automation behavior.
* This will be extended as we build integration into other backend provisioning mechanisms (e.g.  Beaker).

## Common Foreman host parameters

  - ```nullos: true/false```
    - *false* = let Foreman own PXE on the primary host interface
    - *true* = remove PXE flag on primary interface if it exists
    - This is automatically set for OpenStack preparation but can be overridden by the user in Foreman UI/CLI.
    - For hosts that have this as false will get excluded from the instackenv.json (and treated as undercloud host(s))
    - Setting this to false can be useful for excluding a host or a set of hosts to be used for other purposes besides openstack but still be maintained within the same cloud assignment and VLAN networks.
