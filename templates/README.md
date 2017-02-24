Provisioning Templates
======================

This includes snippets, templates and provisioning system-specific files.

* Right now this just contains Foreman snippets we might use or host parameters we depend upon for certain automation behavior.
* This will be extended as we build integration into other backend provisioning mechanisms (e.g.  Beaker).

## Common Foreman host parameters
  - ```undercloud: true/false```
    - controls whether a host should be ommitted from the generated ```instackenv.json```
    - to be available in [RFE #31](https://github.com/redhat-performance/quads/issues/31)
    - *true* = machine will not be listed in generated ```instackenv.json``` to be used as an Overcloud node.
    - *false* = machine will be available as an Overcloud node.
      - This means that the first machine in your allocation will be designated as the undercloud **(default)**

  - ```nullos: true/false```
    - (Dell machines only) tracks whether Ansible iDRAC playbooks should run to remove Foreman PXE flag on primary network interfaces in preparation for OSP Director.
    - *false* = let Foreman own PXE on the primary host interface
    - *true* = remove PXE flag on primary interface if it exists
    - This is automatically set for OpenStack preparation but can be overridden by the user in Foreman UI/CLI.
