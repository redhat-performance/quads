Provisioning Templates
======================

This includes snippets, templates and provisioning system-specific files.

* Right now this just contains Foreman snippets we might use or host parameters we depend upon for certain automation behavior.

## Contents

* ```foreman-post-configure-snippet.rb```
  - Example post-network configuration where we lay down `/etc/sysconfig/network-scripts/ifcfg-*` static network configs for QUADS validations on internal VLAN interfaces.

* ```custom-generic-network-post.rb```
  - Additional templating for mapping interface names based on EL major distribution and system type.`
