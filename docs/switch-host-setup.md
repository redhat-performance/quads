QUADS Bare-Metal Switch and Host Setup
======================================

General guidelines of how to setup your network switches, servers and DNS for QUADS.

![quads](../image/quads.jpg?raw=true)

   * [QUADS Bare-Metal Switch and Host Setup](#quads-bare-metal-switch-and-host-setup)
      * [Network Architecture](#network-architecture)
      * [Physical Switch Setup](#physical-switch-setup)
      * [Distribution Switch Configuration](#distribution-switch-configuration)
      * [TOR Switch Configuration](#tor-switch-configuration)
      * [Greenfield TOR Switch Configuration](#greenfield-tor-switch-configuration)
      * [QUADS Host Network Setup](#quads-host-network-setup)
      * [Adding New QUADS Host](#adding-new-quads-host)
        * [Integration into Foreman or a Provisioning System](#integration-into-foreman-or-a-provisioning-system)
        * [Create Foreman Roles and Filters](#create-foreman-roles-and-filters)
        * [Adding New QUADS Host IPMI](#adding-new-quads-host-ipmi)
          * [Add Optional SSH Keys](add-optional-ssh-keys)
          * [Create QUADS IPMI Credentials](create-quads-ipmi-credentials)

## Network Architecture
   - We use top-of-rack switches that connect up to two distribution switches (Juniper QFX5200 currently)
   - Each TOR switch is uplinked to a pair of distribution (QFX5200 also) configured via MC-LAG

## Physical Switch Setup
   * Connect the serial console for remote management
   * Connect 100gigE optics for uplinks and fiber cable (or appropriate for your environment) - we use 4 x optics per rack.
   * Add ssh keys to your switches for management
```
set system login user quads uid 2002
set system login user quads class super-user
set system login user quads authentication ssh-rsa "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAgEAtX0bAdKVSDeQa4PCN4bLLAqjR0DExUB1lhG1q4jPf9tWwWJ1cRqG3wn7CEqlItiankKdqd+8eZHTGgmBft76
XhjiXtwR4VkANjAqJUFXTkgSXj9nz0rkrHGVYYWvPBvg5KiZm5/ba+ndvyQWc5vDhv8dIKo17uZ5DC6DOcCQs4y6QhYxxVAiqIZaFeFkgRw4Ebkx+MhZ1VrVByOC2PZtj2drwGAa7ItX2i4idIaKTRBI9pehL4ay4NGbzdUeEP304X
k5vwnxBvDBE2oOuZFguQFyNAOkvy+61Tnp6waE05Ss/ZU3J861+fiCJJ1o3waas80qOAIwVTaIwGQ/FTJngZutRcLkdTC21+qaRbW9ZbTIG+bUp1NKAhj84HSsNc8CTcwNEcv8nwi0Cy4ZXY88+DcO5n6CmFFOm7sXTr0umrhBsKTh
Le+f24Xm77cBE5qNleFns7hkPZxRqEznC0xdd1xKswexbAB9mb2vP3uy1qzk3yQsifatzX3qANWrNgjQlALFXEf95woncUY+VA95Y028YM0/ojpi57jq7wHImh9iqzli20G9RE= quads@example.com"
```
   * You may also want a ```~/.ssh/config``` entry for each of your switches to make things easier.

```
Host 10.12.67.247
     User                       quads
     IdentityFile               /root/.ssh/id_rsa_quads
     UserKnownHostsFile         /dev/null
     StrictHostKeyChecking      false
     PubkeyAcceptedKeyTypes=+ssh-dss
```

## Distribution Switch Configuration
   * Configure your switch ports for QUADS-managed hosts as follows, we are using ```et-0/0/12``` on both distribution switches for an example rack.
      * Note: ```interface-range``` identiftier is unique, so for example uplinks for B07 would be PC44 and ae44

```
set interfaces interface-range PC43 member et-0/0/12
set interfaces interface-range PC43 apply-macro do-not-expand
set interfaces interface-range PC43 description sw13-access-scalelab
set interfaces interface-range PC43 ether-options 802.3ad ae43
set interfaces ae43 apply-groups MCAE
set interfaces ae43 apply-groups ACCESS_TRUNK
set interfaces ae43 description sw13-access-scalelab
set interfaces ae43 mtu 9216
set interfaces ae43 aggregated-ether-options lacp active
set interfaces ae43 aggregated-ether-options lacp admin-key 43
set interfaces ae43 aggregated-ether-options mc-ae mc-ae-id 43
```

## TOR Switch Configuration
   * You can easily capture the configuration of an existing QUADS switch with these commands
   * Alter any interface or IP address configuration so that it's unique to your new switch

```
set cli screen-length 0
show configuration | display set
```

## Greenfield TOR Switch Configuration
This configuration is for a brand new switch and you have no others from where you can copy and modify the configuration.
   * Set chassis and channel speed appropriately

```
set chassis redundancy graceful-switchover
set chassis aggregated-devices ethernet device-count 448
set chassis fpc 0 pic 0 port-range 0 29 channel-speed 10g
```

   * Define your uplink interfaces to the distribution switches, do this for both sets.

```
set interfaces interface-range PC1 member et-0/0/31
set interfaces interface-range PC1 member et-0/0/30
set interfaces interface-range PC1 apply-macro do-not-expand
set interfaces interface-range PC1 description sw01-dist-scalelab
set interfaces interface-range PC1 ether-options 802.3ad ae1
```
   * QinQ Group Settings and Port Prefixes
      * We use 100/40GbE breakout cables to split 1 x 40/100G port into many
      * ```xe-0/0/0:0``` is the channel 0 (there are 4 channels, 0,1,2,3) from a breakout cable.
      * ```et``` is generally 40 or 100GbE, ```xe``` is 10GbE
         * e.g. 2 x 40GbE breakout cables turns into 8 x 10GbE ports

   * Create a set of QinQ VLAN group for each QUADS Assignment/Cloud that you intend to use.
   * We use vl1140, vl1150, vl1160, vl1170 and so on.
```
set groups QinQ_vl1140 interfaces <*> flexible-vlan-tagging
set groups QinQ_vl1140 interfaces <*> native-vlan-id 1140
set groups QinQ_vl1140 interfaces <*> mtu 9216
set groups QinQ_vl1140 interfaces <*> encapsulation extended-vlan-bridge
set groups QinQ_vl1140 interfaces <*> unit 0 vlan-id-list 1-4000
set groups QinQ_vl1140 interfaces <*> unit 0 input-vlan-map push
set groups QinQ_vl1140 interfaces <*> unit 0 output-vlan-map pop
```
   * QUADS will apply/unapply QinQ Group Settings for you when things are moved.
   * **Do not paste this below, it's an example**
   * _Done manually it would look like this for example_
```
set interfaces xe-0/0/0:0 apply-groups QinQ_vl1140
set interfaces xe-0/0/0:1 apply-groups QinQ_vl1140
set interfaces xe-0/0/0:2 apply-groups QinQ_vl1140
set interfaces xe-0/0/0:3 apply-groups QinQ_vl1140
set interfaces xe-0/0/1:0 apply-groups QinQ_vl1140
set interfaces xe-0/0/1:1 apply-groups QinQ_vl1140
set interfaces xe-0/0/1:2 apply-groups QinQ_vl1140
set interfaces xe-0/0/1:3 apply-groups QinQ_vl1140
```

## QUADS Host Network Setup
*  QUADS host interface information is now kept in the QUADS database, you can define this afterward at the time of defining your QUADS-managed host.  Refer to the host interface section of the [QUADS Usage Documentation](https://github.com/redhat-performance/quads/tree/master#quads-usage-documentation) after following the rest of this document.

## Adding New QUADS Host
* Rack the new systems to be added to QUADS
  * The provisioning interface is typically wired into a 1GbE NIC and connected to a switch **not** managed by QUADS.
  * Create DNS records using the following name format (in Foreman a new host entry will work)
  * If you already have your own naming convention then CNAMES will work.
```
(rack name)-h(u-location)-(system type)-(domain)
```
```
b08-h13-r620.rdu.openstack.engineering.example.com
```

* Optional PDU power management configuration
  * ~~Once the host is added, and if you have pdu_management enabled, you will also want to ensure you have your host PDU connections mapped out.  For more information on how to setup the PDU-connections.txt file please refer to [docs/pdu-setup.md](https://github.com/redhat-performance/quads/docs/pdu-setup.md)~~

  * **NOTE** As of `1.1.0` PDU management is currently unavailable but will be added back in soon.

### Sending Notification Emails from a Container
   * If you want to send email from QUADS containers (and not the localhost MTA) you will need changes to the localhost MTA of the host running your docker container to facilitate relaying mail through it, as cgroup and container isolation do not permit this without additional settings.
      * In `/etc/postfix/main.cf` where `172.17.0.1` is your `docker0` interface on the docker container host.
      * In our R&D environments we use an upstream SMTP relay server, your environment may vary.
```
inet_interfaces = all
mydestination =
local_recipient_maps =
mynetworks = 172.17.0.0/16, localhost, 127.0.0.0/8
relay_domains = domain.example.com, example.com
relayhost = [ipaddress.of.your.relay.smtp.server]
smtpd_recipient_restrictions = permit_mynetworks
smtpd_authorized_xforward_hosts = [::1]/128
smtpd_client_restrictions =
```

### Integration into Foreman or a Provisioning System
   * We will not be covering setting up [Foreman](https://theforeman.org) however that is documented [extensively here](https://theforeman.org/manuals/1.15/index.html).
   * We do provide some [example templates](https://github.com/redhat-performance/quads/tree/master/templates) for post-provisioning creation of system interface config files like ```/etc/sysconfig/network-scripts/ifcfg-*``` for use with QUADs.

### Create Foreman Roles and Filters
   * This is Foreman-specific so if you want another provisioning backend you can ignore it.
   * We use RBAC roles and filters to allow per-cloud Foreman views into subsets of machines, QUADS will manage this for you once created.
      * Each server has a role named after it
      * Each server role has filters attached that grant it certain permissions
   * Create a role per server
```
hammer role create --name host01.example.com
```
   * Create a filter with access permissions and associate it with that role
```
hammer filter create --role host01.example.com --search "name = host01.example.com" --permissions view_hosts,edit_hosts,build_hosts,power_hosts,console_hosts --role-id $(hammer role info --name host01.example.com | egrep ^Id: | awk '{ print $NF }')
```
   * Next you'll need to make a Foreman user per unique cloud environment if they don't exist already
```
hammer user create --login cloud01 --password password --mail quads@example.com --auth-source-id 1
hammer user create --login cloud02 --password password --mail quads@example.com --auth-source-id 1
hammer user create --login cloud03 --password password --mail quads@example.com --auth-source-id 1
```

   * Lastly you will need to provide a special group these users belong to for generic, persistent filters cloud users will always need.

```
hammer role create --name clouduser_views
hammer filter create --role clouduser_views --permissions view_operatingsystems
```
   * Now you'll need to update the filters associated with the `cloudusers_views` role with other resource types.
```
hammer filter update --role clouduser_views --permissions view_architectures --id $(hammer filter list | grep clouduser_views | awk '{print $1}')
hammer filter update --role clouduser_views --permissions view_media --id $(hammer filter list | grep clouduser_views | awk '{print $1}')
hammer filter update --role clouduser_views --permissions view_ptables --id $(hammer filter list | grep clouduser_views | awk '{print $1}')
hammer filter update --role clouduser_views --permissions edit_params,view_params --id $(hammer filter list | grep clouduser_views | awk '{print $1}')
```
   * Your filters should look something like this when you're done, this can also be done in the Foreman UI as well.

![clouduser_rbac](../image/cloud_rbac.png?raw=true)

   * Next create your `cloudusers` generic group and tie it all together
```
hammer user-group create --name cloudusers --roles clouduser_views
```
   * Lastly, add all your existing cloud users as members of this group (we use 32 cloud users in this example)
```
for clouduser in $(seq 1 9); do hammer user-group add-user --name cloudusers --user cloud0$clouduser; done
for clouduser in $(seq 10 32); do hammer user-group add-user --name cloudusers --user cloud$clouduser; done
```

### Adding New QUADS Host IPMI

#### Add Optional SSH Keys

   * Ensure QUADS host has access to the out-of-band interfaces
      * For Dell systems we copy the QUADS ssh key in via racadm
```
/opt/dell/srvadmin/bin/idracadm -r <drac IP> -u root -p calvin sshpkauth -f /root/.ssh/id_rsa_r620.pub -i 2 -k 1
```
   * Refer to your vendor out-of-band documentation for other system types if you want to add ssh keys.

#### Create QUADS IPMI Credentials
   * IPMI credentials are defined in [the QUADS configuration file](https://github.com/redhat-performance/quads/blob/master/conf/quads.yml#L138) so adjust accordingly to your environment and preference.
   * Note: SuperMicro systems (and perhaps other vendors) do not have the `root` user by default, if not you'll need to create it.
   * Check if the `root` user exists first, Dell systems come with a `root` user by default so this step can be omitted.

```
ipmitool -I lanplus -H mgmt-<hostname> -U ADMIN -P ADMIN  user list | grep root
```

   * Note: SuperMicro systems (and perhaps other vendors) do not have the `root` user by default, if not you'll need to create it.

```
ipmitool -I lanplus -H mgmt-<hostname> -U ADMIN -P ADMIN  user set name 3 root
ipmitool -I lanplus -H mgmt-<hostname> -U ADMIN -P ADMIN  user set password 3 YourRootPass
ipmitool -I lanplus -H mgmt-<hostname> -U ADMIN -P ADMIN user priv 3 0x4
ipmitool -I lanplus -H mgmt-<hostname> -U ADMIN -P ADMIN channel setaccess 1 3 ipmi=on
```

   * Create a ```quads``` IPMI user on all out-of-band interfaces with the proper privileges

```
ipmitool -I lanplus -H mgmt-<hostname> -U root -P <pw> user set name 4 quads
ipmitool -I lanplus -H mgmt-<hostname> -U root -P <pw> user set password 4 quads
ipmitool -I lanplus -H mgmt-<hostname> -U root -P <pw> user priv 4 0x4
ipmitool -I lanplus -H mgmt-<hostname> -U root -P <pw> user enable 4
ipmitool -I lanplus -H mgmt-<hostname> -U root -P <pw> channel setaccess 1 4 ipmi=on
```

At this point you can proceed with initializing QUADS [from the main documentation](https://github.com/redhat-performance/quads#quads-usage-documentation)
