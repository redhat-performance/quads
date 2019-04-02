QUADS (quick and dirty scheduler)
====================================

Automate scheduling and end-to-end provisioning of servers and networks.

* Visit the [QUADS blog](https://quads.dev)
* Please read our [contributing guide](https://github.com/redhat-performance/quads/blob/master/CONTRIBUTING.md) and use [Gerrit Review](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) to submit patches.

![quads](/image/quads.jpg?raw=true)

![quads-rpm-build](https://copr.fedorainfracloud.org/coprs/quadsdev/python3-quads/package/quads/status_image/last_build.png)

   * [QUADS (quick and dirty scheduler)](#quads-quick-and-dirty-scheduler)
      * [What does it do?](#what-does-it-do)
      * [Design](#design)
      * [Requirements](#requirements)
      * [QUADS Workflow](#quads-workflow)
      * [QUADS Switch and Host Setup](#quads-switch-and-host-setup)
      * [Installing QUADS](#installing-quads)
         * [Installing QUADS with Docker Compose](#installing-quads-with-docker-compose)
         * [Installing QUADS from Github](#installing-quads-from-github)
         * [Installing QUADS from RPM](#installing-quads-from-rpm)
      * [QUADS Usage Documentation](#quads-usage-documentation)
         * [How Provisioning Works](#how-provisioning-works)
            * [QUADS Move Host Command](#quads-move-host-command)
      * [Common Administration Tasks](#common-administration-tasks)
         * [Creating a New Cloud Assignment and Schedule](#creating-a-new-cloud-assignment-and-schedule)
            * [QUADS VLAN Options](#quads-vlan-options)
            * [Defining a New Cloud](#defining-a-new-cloud)
            * [Adding New Hosts to your Cloud](#adding-new-hosts-to-your-cloud)
         * [Extending the <strong>Schedule</strong> of an Existing
           Cloud](#extending-the-schedule-of-an-existing-cloud)
         * [Extending the <strong>Schedule</strong> of Existing Cloud with Differing Active Schedules](#extending-the-schedule-of-existing-cloud-with-differing-active-schedules)
         * [Extending Machine Allocation to an existing Cloud](#extending-machine-allocation-to-an-existing-cloud)
         * [Removing a Schedule](#removing-a-schedule)
         * [Removing a Schedule across a large set of hosts](#removing-a-schedule-across-a-large-set-of-hosts)
         * [Removing a Host from QUADS](#removing-a-host-from-quads)
      * [Using the QUADS JSON API](#using-the-quads-json-api)
      * [Additional Tools and Commands](#additional-tools-and-commands)
         * [Looking into the Future](#looking-into-the-future)
         * [Dry Run for Pending Actions](#dry-run-for-pending-actions)
         * [Find Free Cloud Environment](#find-free-cloud-environments)
         * [Find Available Hosts](#find-available-hosts)
      * [Interacting with MongoDB](#interacting-with-mongodb)
         * [Example: Change the wipe value in MongoDB](#example-change-the-wipe-value-in-mongodb)
         * [Example: Querying Notification Values in MongoDB](#example-querying-notification-values-in-mongodb)
      * [Backing up QUADS](#backing-up-quads)
      * [Restoring QUADS DB from Backup](#restoring-quads-db-from-backup)
      * [QUADS Talks and Media](#quads-talks-and-media)

## What does it do?
   - Create and manage a date/time schedule for machine allocations
   - Drive system provisioning and network switch changes based on workload assignment via external commands
   - Control PDU sockets for connected bare-metal systems for power actions
   - Automated network and provisioning validation prior to delivering sets of machines/networks to users.
   - Generates instackenv.json for each OpenStack environment.
   - Automatically generate documentation to illustrate current status, published to a [Wordpress instance](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html#pages)
     * Current system details
     * Current workloads and assignments
     * Current ownership and resource utilization links (grafana/collectd)
     * Total duration and time remaining in system assignments
     * Dynamic provisioning & system/network validation status per assignment
     * Granular Ansible facts inventory per server via [ansible-cmdb](https://github.com/fboender/ansible-cmdb)
   - Query scheduling data to determine future availability
   - Generates a monthly, auto-updated calendar of machine assignments
   - Generates a per-month visualization map for per-machine allocations to assignments.
   - RT (or similiar ticketing system) integration.
   - IRC bot and email notifications for new provisioning tasks and ones ending completion

## Design
   - Main components: `Python3, Cherrypy, Mongoengine, MongoDB, Jinja2`
   - Installation via Docker compose, RPM (Fedora or EL8+) or Github sources
   - We use [badfish](https://github.com/redhat-performance/badfish) for managing bare-metal IPMI
   - We use [Foreman](https://theforeman.org/) for the systems provisioning backend.
   - We use [Wordpress](https://wordpress.org/) for auto-generating wiki and documentation.
   - A typical container-based QUADS deployment might look like this:

![quadsarchitecture](/image/quads-container-architecture.png?raw=true)

## Requirements
   - In QUADS 1.1+ we are using Python3, Cherrypy and Jinja2 with MongoDB as the database backend.
   - The scheduling functionality can be used standalone, but you'll want a provisioning backend like [Foreman](https://theforeman.org/) to take full advantage of QUADS scheduling, automation and provisioning capabilities.
   - To utilize the automatic wiki/docs generation we use [Wordpress](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/) but anything that accepts markdown via an API should work.
   - Switch/VLAN automation is done on Juniper Switches in [Q-in-Q VLANs](http://www.jnpr.net/techpubs/en_US/junos14.1/topics/concept/qinq-tunneling-qfx-series.html), but commandsets can easily be extended to support other network switch models.
   - We use [badfish](https://github.com/redhat-performance/badfish) for optional Dell playbooks to toggle boot order and PXE flags to accomodate OpenStack deployments via Ironic/Triple-O.
   - The package [ansible-cmdb](https://github.com/fboender/ansible-cmdb) needs to be available if you want to see per assignment Ansible facts of the inventory. It can be obtained from [here](https://github.com/fboender/ansible-cmdb/releases)

## QUADS Workflow

You can read about QUADS architecture, provisioning, visuals and workflow [in our documentation examples and screenshots](/docs/quads-workflow.md)

## QUADS Switch and Host Setup
   - To ensure you have setup your switch properly please follow our [Switch and Host Setup Docs](/docs/switch-host-setup.md)

## Installing QUADS
   - We offer Docker compose, RPM packages or a Git clone installation (for non RPM-based distributions, BSD UNIX, etc).
   - It's recommended to use the Docker method as it requires less setup.

### Installing QUADS with Docker Compose
   - Clone the QUADS Github repository
```
git clone --single-branch --branch master https://github.com/redhat-performance/quads /opt/docker/quads
```
   - Read through the [QUADS YAML configuration file](/conf/quads.yml) for other settings you way want.
   - Make a copy of it and place it on the local filesystem of the Docker host outside the git checkout
```
mkdir -p /opt/quads/conf
cp /opt/docker/quads/conf/quads.yml /opt/quads/conf/quads.yml
```
   - Make any changes required to your `/opt/quads/conf/quads.yml`
```
vi /opt/quads/conf/quads.yml
```
   - Run docker-compose to bring up a full QUADS stack
```
docker-compose -f /opt/docker/quads/docker/docker-compose-production.yml up -d
```
   - Access Quads Wiki via browser at `http://localhost` or `http://quads-container-host` to setup your Wiki environment.
   - Run commands against containerized quads via docker exec

```
docker exec quads bin/quads-cli --define-cloud cloud01 --description cloud01
```

   * Container Layout

| Container | Purpose | Source Image | Name |
|-----------|---------|--------------|----------------------|
| quads | quads server | Official Python3 Image | python:3 |
| quads_db  | quads database | Official Mongodb Image | mongo:4.0.4-xenial |
| nginx | wiki proxy| Official Nginx Image | nginx:1.15.7-alpine |
| wiki | quads wiki | Official WP Image | wordpress:5.0.0-php5.6-fpm-alpine |
| wiki_db | wiki database | Official MariaDB Image | mariadb ||

We find it useful to create an alias on your quads container for executing quads-cli commands inside the container.

   - On your docker host:
```
echo 'alias quads="docker exec -it quads bin/quads-cli"' >> ~/.bashrc
```

   - e.g. creating an environment and adding hosts
```
quads --define-cloud cloud01 --description "spare pool"
quads --add-host host01 --default-cloud cloud01 --host-type general
```

### Installing QUADS from Github
This method requires you to satisfy all of your Python3 and library dependencies yourself and isn't recommended, however it probably is the only way to run QUADS on some platforms like FreeBSD.  Substitute package names and methods appropriately.

   - Clone the git repository (substitute paths below as needed)

```
git clone https://github.com/redhat-performance/quads /opt/quads
```
   - Install pre-requisite Python packages
```
dnf install python3-requests python3-wordpress-xmlrpc python3-pexpect python3-paramiko ipmitool python3-cherrypy python3-mongoengine mongodb mongodb-server python3-jinja2 python3-passlib python3-PyYAML python3-requests python3-GitPython
```
   - Install a webserver (Apache, nginx, etc)
```
dnf install httpd
```
   - Create logging directory (you can edit this in ```conf/quads.yml``` via the ```log:``` parameter).
```
mkdir -p /opt/quads/log
```
   - Create your visualization web directory (you can configure this in ```conf/quads.yml``` via ```visual_web_dir```)
```
mkdir -p /var/www/html/visual
```
   - Populate the web visualization images in your webserver directory
```
cp -p /opt/quads/images/{button*,texture*}.png /var/www/html/visual/
```
   - Read through the [QUADS YAML configuration file](/conf/quads.yml) for other settings you way want.
```
vi /opt/quads/conf/quads.yml
```
   - Enable and start the QUADS systemd service (daemon)
   - Note: You can change QUADS ```quads_base_url``` listening port in ```conf/quads.yml``` and use the ```--port``` option
```
cp /opt/quads/systemd/quads-server.service /etc/systemd/system/quads-server.service
systemctl daemon-reload
systemctl enable quads-server.service
systemctl start quads-server.service
```
   - Note: You can use QUADS on non-systemd based Linux or UNIX distributions but you'll need to run ```/opt/quads/bin/quads-server``` via an alternative init process or similiar functionality.

### Installing QUADS from RPM
   - We build RPM packages for Fedora and CentOS/RHEL 8
   - On Fedora30 and above you'll need to manually install mongodb first, see [installing mongodb for QUADS](docs/install-mongodb.md)
   - On RHEL/CentOS8 you'll need to install MongoDB first via `dnf install mongodb mongodb-server`

* Once you have mongodb installed and running you can install/upgrade QUADS via RPM.

```
dnf copr enable quadsdev/python3-quads  -y
dnf install quads -y
```
   - Read through the [QUADS YAML configuration file](/conf/quads.yml)
```
vi /opt/quads/conf/quads.yml
```
   - Enable and Start dependent services
   - [haveged](https://issihosts.com/haveged/) is a replacement entropy service for VM's, it's optional so turn it off if you want to use `/dev/random` - this solves certain [performance issues](https://github.com/redhat-performance/quads/issues/221) known to occur with lack of entropy when running QUADS in a VM.
```
systemctl enable httpd
systemctl enable haveged
systemctl start haveged
systemctl start httpd
systemctl start mongod
```
   - Enable and start the QUADS systemd service (daemon)
   - Note: You can change QUADS ```quads_base_url``` listening port in ```conf/quads.yml``` and use the ```--port``` option
```
systemctl enable quads-server
systemctl start quads-server
```
   - Source quads binaries in your $PATH (or login with another shell)
```
source /etc/profile.d/quads.sh
```
   - Now you're ready to go.
```
quads-cli --help
```
   - For full functionality with Foreman you'll also need to have [hammer cli](https://theforeman.org/2013/11/hammer-cli-for-foreman-part-i-setup.html) installed and setup on your QUADS host.

   - Note: RPM installations will have ```quads-cli``` and tools in your system $PATH but you will need to login to a new shell to pick it up.  We typically place this as an alias in `/root/.bashrc`.
```
echo 'alias quads="quads-cli"' >> /root/.bashrc
```

### Installing other QUADS Components
#### QUADS Wiki
   - There is also a Wordpress Wiki [VM](https://github.com/redhat-performance/ops-tools/tree/master/ansible/wiki-wordpress-nginx-mariadb) QUADS component that we use a place to automate documentation via a Markdown to Python RPC API but any Markdown-friendly documentation platform could suffice.  Note that the container deployment sets this up for you.
   - You'll then simply need to create an `infrastructure` page and `assignments` page and denote their `page id` for use in automation.  This is set in `conf/quads.yml`
   - We also provide the `krusze` theme which does a great job of rendering Markdown-based tables, and the `JP Markdown` plugin which is required to upload Markdown to the [Wordpress XMLRPC Python API](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/)
   - On CentOS/RHEL7 you'll need the [python2-wordpress-xmlrpc](https://github.com/redhat-performance/ops-tools/raw/master/packages/python2-wordpress-xmlrpc-2.3-11.fc28.noarch.rpm) package unless you satisfy it with pip.
   - You'll also need `bind-utils` package installed that provides the `host` command

#### Foreman Hammer CLI
   - For full Foreman functionality you'll want to have a working [hammer cli](https://theforeman.org/2013/11/hammer-cli-for-foreman-part-i-setup.html) setup on your QUADS host as well.

#### Ansible CMDB
   - We use the [Ansible CMDB](https://github.com/fboender/ansible-cmdb) project as an additional validation step and to generate a one-time Ansible facts-generated web page for all the hosts in each QUADS assignment.
   - Install the package for this or consume it via Github.

```
yum install ansible https://github.com/fboender/ansible-cmdb/releases/download/1.27/ansible-cmdb-1.27-2.noarch.rpm
```
   - You can turn off this functionality in `/opt/quads/conf/quads.yml` via `gather_ansible_facts: false`

#### QUADS Move Command
   - QUADS relies on calling an external script, trigger or workflow to enact the actual provisioning of machines. You can look at and modify our [move-and-rebuild-host](https://github.com/redhat-performance/quads/blob/master/bin/move-and-rebuild-host.sh) script to suit your environment for this purpose.  Read more about this in the [move-host-command](https://github.com/redhat-performance/quads#quads-move-host-command) section below.

   - Note: RPM installations will have ```quads-cli``` and tools in your system $PATH but you will need to login to a new shell to pick it up.

## QUADS Usage Documentation

   - Define the various cloud environments
   - These are the isolated environments QUADS will use and provision into for you.

```
quads-cli --define-cloud cloud01 --description "Primary Cloud Environment"
quads-cli --define-cloud cloud02 --description "02 Cloud Environment"
quads-cli --define-cloud cloud03 --description "03 Cloud Environment"
```

   - Define the hosts in the environment (Foreman Example)
     - Note the ```--host-type``` parameter, this is a mandatory, free-form label that can be anything.  It will be used later for ```post-config``` automation and categorization.
     - If you don't want systems to be reprovisioned when they move into a cloud environment append ``--no-wipe` to the define command.
     - We are excluding anything starting with mgmt- and including servers with the name r630.

```
for h in $(hammer host list --per-page 1000 | egrep -v "mgmt|c08-h30"| grep r630 | awk '{ print $3 }') ; do quads-cli --define-host $h --default-cloud cloud01 --host-type general; done
```

   - The command without Foreman would be simply:

```
quads-cli --define-host <hostname> --default-cloud cloud01 --host-type general
```

   - Define the host interfaces, these are the internal interfaces you want QUADS to manage for VLAN automation
   - Note that `--interface-ip` corresponds to the IP of the switch that hosts interface is connected to.
   - Do this for every interface you want QUADS to manage per host (we are working on auto-discovery of this step).

```
quads-cli --add-interface em1 --interface-mac 52:54:00:d9:5d:df --interface-ip 10.12.22.201 --interface-port xe-0/0/1:0 --host <hostname>
quads-cli --add-interface em2 --interface-mac 52:54:00:d9:5d:dg --interface-ip 10.12.22.201 --interface-port xe-0/0/1:1 --host <hostname>
quads-cli --add-interface em3 --interface-mac 52:54:00:d9:5d:dh --interface-ip 10.12.22.201 --interface-port xe-0/0/1:2 --host <hostname>
quads-cli --add-interface em4 --interface-mac 52:54:00:d9:5d:d1 --interface-ip 10.12.22.201 --interface-port xe-0/0/1:3 --host <hostname>
```

   - To list the hosts:

```
quads-cli --ls-hosts
```
You will now see the list of full hosts.

```
c08-h21-r630.example.com
c08-h22-r630.example.com
c08-h23-r630.example.com
c08-h24-r630.example.com
c08-h25-r630.example.com
c08-h26-r630.example.com
c08-h27-r630.example.com
c08-h28-r630.example.com
c08-h29-r630.example.com
c09-h01-r630.example.com
c09-h02-r630.example.com
c09-h03-r630.example.com
```

   - To list a hosts interface and switch information:

```
quads --ls-interface --host c08-h21-r630.example.com

{"name": "em1", "mac_address": "52:54:00:d9:5d:df", "ip_address": "10.12.22.201", "switch_port": "xe-0/0/1:0"}
{"name": "em2", "mac_address": "52:54:00:d9:5d:dg", "ip_address": "10.12.22.201", "switch_port": "xe-0/0/1:1"}
{"name": "em3", "mac_address": "52:54:00:d9:5d:dh", "ip_address": "10.12.22.201", "switch_port": "xe-0/0/1:2"}
{"name": "em4", "mac_address": "52:54:00:d9:5d:d1", "ip_address": "10.12.22.201", "switch_port": "xe-0/0/1:3"}
```

   - To see the current system allocations:

```
quads-cli --summary
```
```
cloud01 : 45 (Primary Cloud Environment)
cloud02 : 0 (02 Cloud Environment)
cloud03 : 0 (03 Cloud Environment)
```
   - Define a custom schedule for a host
     - Example: assign host ```c08-h21``` to the workload/cloud ```cloud02```

```
quads-cli --add-schedule --host c08-h21-r630.example.com --schedule-start "2016-07-11 08:00" --schedule-end "2016-07-12 08:00" --schedule-cloud cloud02
```

   - List the schedule for a specific host:

```
quads-cli --ls-schedule --host c08-h21-r630.example.com
```

You'll see the schedule output below

```
Default cloud: cloud01
Current cloud: cloud02
Defined schedules:
  0:
    start: 2016-07-11 08:00
    end: 2016-07-12 08:00
    cloud: cloud02
```

   - Move any hosts that need to be re-allocated based on the current schedule

```
quads-cli --move-hosts
```

You should see the following verbosity from a move operation

```
INFO: Moving c08-h21-r630.example.com from cloud01 to cloud02 c08-h21-r630.example.com cloud01 cloud02
```

### How Provisioning Works
#### QUADS move host command
In the above example the default move command called ```/bin/echo``` for illustration purposes.  In order for this to do something more meaningful you should invoke a script with the ```--move-command``` option, which should be the path to a valid command or provisioning script/workflow.

* Define your move command by pointing QUADS to an external command, trigger or script.
* This expects three arguments `hostname current-cloud new-cloud`.

```
quads-cli --move-hosts --path-to-command /opt/quads/bin/move-and-rebuild-host.sh
```

* You can look at the [move-and-rebuild-host](https://github.com/redhat-performance/quads/blob/master/bin/move-and-rebuild-host.sh) script as an example.  It's useful to note that with `bin/move-and-rebuild-host.sh` passing a fourth argument will result in only the network automation running and the actual host provisioning will be skipped.  You should review this script and adapt it to your needs, we try to make variables for everything but some assumptions are made to fit our running environments.

## Common Administration Tasks

### Creating a New Cloud Assignment and Schedule

Creating a new schedule and assigning machines is currently done through the QUADS CLI.  There are a few options you'll want to utilize.  Mandatory options are in bold and optional are in italics.

   -  **description** (this will appear on the assignments dynamic wiki)
   -  **cloud-owner** (for associating ownership and usage notifications)
   -  *force* (needed for re-using an existing cloud)
   -  *cc-users* (Add additional people to the notifications)
   -  *cloud-ticket* (RT ticket used for the work, also appears in the assignments dynamic wiki)
   -  *wipe* (whether to reprovision machines going into this cloud, default is 1 or wipe.

#### QUADS VLAN Options ####
   -  VLAN design (optional, will default to 0 below)
     - ```qinq: 0``` (default) qinq VLAN separation by interface: primary, secondary and beyond QUADS-managed interfaces all match the same VLAN membership across other hosts in the same cloud allocation.  Each interface per host is in its own VLAN, and these match across the rest of your allocated hosts by interface (all nic1, all nic2, all nic3, all nic4 etc).
     - ```qinq: 1``` all QUADS-managed interfaces in the same qinq VLAN

#### Defining a New Cloud ####

```
quads-cli --define-cloud cloud03 --description "Messaging AMQ" --force --cloud-owner epresley --cc-users "jdoe jhoffa" --cloud-ticket 423625 --qinq 0
```

   - Now that you've defined your new cloud you'll want to allocate machines and a schedule.
     - We're going to find the first 20 Dell r620's and assign them as an example.

#### Adding New Hosts to your Cloud ####
```
quads-cli --cloud-only cloud01 | grep r620 | head -20 > /tmp/RT423624
```

   - Now we'll allocate all of these hosts with a schedule, by default our system times use UTC.

```
for h in $(cat /tmp/RT423624) ; do quads-cli --host $h --add-schedule --schedule-start "2016-10-17 00:00" --schedule-end "2016-11-14 17:00" --schedule-cloud cloud03 ; done
```

That's it.  At this point your hosts will be queued for provision and move operations, we check once a minute if there are any pending provisioning tasks.  To check manually:

```
quads-cli --move-hosts --dry-run

```

After your hosts are provisioned and moved you should see them populate under the cloud list.

```
quads-cli --cloud-only cloud03
```

### Extending the __Schedule__ of an Existing Cloud

Occasionally you'll want to extend the lifetime of a particular assignment. QUADS lets you do this with one command but you'll want to double-check things first.
In this example we'll be extending the assignment end date for cloud03

   - First, get the updated list of current assignments

```
quads-cli --summary
```
```
cloud01 : 55 (Pool of available servers)
cloud02 : 12 (Small OSPD deployment)
cloud03 : 20 (Messaging - AMQ - dispatch router and artemis broker)
cloud04 : 60 (Ceph deployment)
cloud07 : 10 (Small OSPD deployment)
cloud09 : 5 (Keystone OSPD deployment)
cloud10 : 14 (Openshift + OSPD testing)
```

   - Next, List the owners of the clouds.

```
quads-cli --ls-owner
```
```
cloud01 : nobody
cloud02 : bjohnson
cloud03 : jhoffa
cloud04 : ltorvalds
cloud05 : nobody
cloud06 : nobody
cloud07 : dtrump
cloud08 : nobody
cloud09 : dtrump
cloud10 : cnorris
```

   - Lastly, obtain a list of the current machines in cloud03

```
quads-cli --cloud-only cloud03
```
```
b09-h01-r620.rdu.openstack.example.com
b09-h02-r620.rdu.openstack.example.com
b09-h03-r620.rdu.openstack.example.com
b09-h05-r620.rdu.openstack.example.com
b09-h06-r620.rdu.openstack.example.com
b09-h07-r620.rdu.openstack.example.com
b09-h09-r620.rdu.openstack.example.com
b09-h11-r620.rdu.openstack.example.com
b09-h14-r620.rdu.openstack.example.com
b09-h15-r620.rdu.openstack.example.com
b09-h17-r620.rdu.openstack.example.com
b09-h18-r620.rdu.openstack.example.com
b09-h19-r620.rdu.openstack.example.com
```

   - Take a look at the existing schedule for one of these machines, you'll see it expires 2016-10-30.

```
quads-cli --host b09-h01-r620.rdu.openstack.example.com --ls-schedule
```
```
Default cloud: cloud01
Current cloud: cloud03
Current schedule: 0
Defined schedules:
  0| start=2016-10-17 00:00,end=2016-10-30 18:00,cloud=cloud03
```

   - Extend the ```--schedule-end``` date for the Cloud

If you are sure you've got the right cloud assignment from above you can proceed
This is the actual command that extends the schedule, the other commands above are more for your verification.
Below we will be extending the schedule end date from 2016-10-30 to 2016-11-27 at 18:00

```
for h in $(quads-cli --cloud-only cloud03) ; do quads-cli --host $h --mod-schedule 0 --schedule-end "2016-11-27 18:00"; done
```

### Extending the __Schedule__ of Existing Cloud with Differing Active Schedules

When in heavy usage some machines primary, active schedule may differ from one another, e.g. 0 versus 1, versus 2, etc.  Because schedules operate on a per-host basis sometimes the same schedule used within a cloud may differ in schedule number.  Here's how you modify them across the board for the current active schedule if the ID differs.

* Example: extend all machines in cloud10 to end on 2017-03-06 22:00 UTC (they previously would end 2019-02-09 22:00)
* These have differing primary active schedule IDs.

  - Check your commands via echo first
  - Reschedule against a certain cloud **and** start date

```
for h in $(quads-cli --cloud-only cloud05); do echo quads-cli --mod-schedule $(quads-cli --ls-schedule --host $h | grep cloud05 | grep "end=2017-02-09" | tail -1 | awk -F\| '{ print $1 }') --host $h --schedule-end "2017-03-06 22:00" ; done
```

  * If all looks good you can remove **remove the echo lines** and apply.

### Extending Machine Allocation to an existing Cloud

QUADS also supports adding new machines into an existing workload (cloud).

   - Search Availability Pool for Free Servers
      - Let's look for any 5 x servers from `2019-03-11 22:00` until `2019-04-22 22:00`

```
quads-cli --ls-available --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00"

```
```
c03-h11-r620.rdu.openstack.example.com
c03-h13-r620.rdu.openstack.example.com
c03-h14-r620.rdu.openstack.example.com
c03-h15-r620.rdu.openstack.example.com
```

  - Move New Hosts into Existing Cloud

Above we see all the free servers during our timeframe, let's move them into cloud10

```
quads-cli --host c03-h11-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads-cli --host c03-h13-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads-cli --host c03-h14-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads-cli --host c03-h15-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
```

### Removing a Schedule

You can remove an existing schedule across a set of hosts using the ```--rm-schedule``` flag against the schedule ID for each particular machine of that assignment.

   - Example: removing the schedule for three machines in cloud
   - Obtain the schedule ID via ```quads-cli --ls-schedule --host```
   - These machines would happen to have the same cloud assignment as schedule id 2.
```
quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
```

### Removing a Schedule across a large set of hosts

You should search for either the start or end dates to select the right schedule ID to remove when performing schedule removals across a large set of hosts.

   - If you are using QUADS in any serious capacity **always pick this option**.
   - Example: removing schedule by searching for start date.
   - Often machine schedule ID's are different for the same schedule across a set of machines, this ensures you remove the right one.

```
for host in $(cat /tmp/452851); do quads-cli --rm-schedule $(quads-cli --ls-schedule --host $host | grep cloud08 | grep "start=2017-08-06" | tail -1 | awk -F\| '{ print $1 }') --host $host ; echo Done. ; done
```

### Removing a Host from QUADS

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```
quads-cli --rm-host f03-h30-000-r720xd.rdu2.example.com
Removed: {'host': 'f03-h30-000-r720xd.rdu2.example.com'}
```

## Using the QUADS JSON API
* All QUADS actions under the covers uses the JSON API v2
   - Please [read about the QUADS RESTful API here](/docs/quads-api.md)
* This is an optional local systemd service you can start and interact with and listens on localhost ```TCP/8080```

## Additional Tools and Commands

### Looking into the Future
* Because QUADS knows about all future schedules you can display what your environment will look like at any point in time using the `--date` command.

* Looking into a specific environment by date

```
quads-cli --cloud-only cloud08 --date "2019-06-04 22:00"
```

```
f16-h01-000-1029u.rdu2.example.com
f16-h02-000-1029u.rdu2.example.com
f16-h03-000-1029u.rdu2.example.com
f16-h05-000-1029u.rdu2.example.com
f16-h06-000-1029u.rdu2.example.com
```

* Looking at all schedules by date

```
quads-cli --ls-schedule --date "2020-06-04 22:00"
```

### Dry Run for Pending Actions
* You can see what's in progress or set to provision via the ```--dry-run``` sub-flag of ```--move-hosts```

```
quads-cli --move-hosts --dry-run
```
```
INFO: Moving b10-h27-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h18-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h19-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h21-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h25-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h26-r620.rdu.openstack.example.com from cloud01 to cloud03
```

### Find Free Cloud Environment

* You can use `quads-cli --find-free-cloud` to suggest a cloud environment to use that does not have any future hosts scheduled to use it.

```
quads-cli --find-free-cloud
```

```
cloud12
cloud16
cloud17
cloud18
```

### Find Available Hosts

* The `--find-available` functionality lets you search for available hosts in the future based on a date range or other criteria.

  - Find based on a date range:

```
quads-cli --ls-available --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00"
```

  - Find based on starting now with an end range:

```
quads --ls-available --schedule-end "2019-06-02 22:00"
```

## Interacting with MongoDB
* In some scenarios you may wish to interrogate or modify values within MongoDB.  You should be careful doing this and have good backups in place.  Generally, we will try to implement data, object and document modification needs through quads-cli so you don't need to do this but sometimes it's useful for troubleshooting or other reasons.

* Example:  Toggling the `wipe:` cloud value that determines whether new systems entering an environment should be reprovisioned or not.  In this example `cloud02` has the value of `wipe: 0` and we want to change this within Mongodb.

   - First run `mongo` to enter cli mode

```
# mongo
MongoDB shell version v4.0.3
connecting to: mongodb://127.0.0.1:27017
Implicit session: session { "id" : UUID("21a4cd3c-e191-4f03-b18c-dccdb55826b3") }
MongoDB server version: 4.0.3
```

   - Next, enter the database

```
> use quads
switched to db quads
```

### Example: Change the wipe value in MongoDB

   - Query the cloud metadata for `cloud02`

```
> db.cloud.find({name: "cloud02"})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "notified" : true, "validated" : true, "released" : true, "name" : "cloud02", "description" : "EL7 to EL8 Satellite Upgrade", "owner" : "ikaur", "ticket" : "490957", "qinq" : true, "wipe" : false, "ccuser" : [ "psuriset" ], "provisioned" : true }
```

   - We want to change `wipe: false` to `wipe: true`

```
> db.cloud.update({name:"cloud02"}, {$set:{wipe:true}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

   - Let's check and make sure it was successful

```
> db.cloud.find({name:"cloud02"})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "notified" : true, "validated" : true, "released" : true, "name" : "cloud02", "description" : "EL7 to EL8 Satellite Upgrade", "owner" : "ikaur", "ticket" : "490957", "qinq" : true, "wipe" : true, "ccuser" : [ "psuriset" ], "provisioned" : true }
```

   - Above, we can see this value was changed.
   - Lastly let's see if `quads-cli` thinks so too.

```
quads-cli --ls-wipe | grep cloud02
cloud02: True
```

* **Disclaimer** Generally you never need to modify things in MongoDB, there should be a `quads-cli` equivalent to do this safely and easily without mucking with the database.  If there's functionality missing here please [file a Github RFE](https://github.com/redhat-performance/quads/issues/new).

* Above, the correct way to adjust this is by redefining your cloud with all the same values but just not specify a wipe value.

```
quads-cli --define-cloud cloud02 --cloud-owner ikaur --force --description "EL7 to EL8 Satellite Upgrade" --cloud-ticket 490957 --cc-users "psuriset"
['Updated cloud cloud02']
```

* Note: if you **did not** want machines entering into a new environment to be wiped/provisioned just use define the environment with the ``--no-wipe` option.

{{{
quads-cli --define-cloud cloud16 --cloud-owner jdoe --force --description "New Environment" --cloud-ticket 012345 --no-wipe
}}}

### Example: Querying Notification Values in MongoDB

* One more example: examining notification status of an assignment

   - We use ticket numbers as one of the metadata criteria to uniquely identify assignments
   - Here we'll query the notification status inside MongoDB for a particular workload.

```
> db.notification.find({ticket:"999999"})
{ "_id" : ObjectId("5ced1d769137063b1cadbc79"), "cloud" : ObjectId("5c82b36e0f767d000692ad0b"), "ticket" : "999999", "fail" : true, "success" : false, "initial" : false, "pre_initial" : true, "pre" : false, "one_day" : false, "three_days" : false, "five_days" : false, "seven_days" : false }
```

## Backing up QUADS

* We do not implement backups for QUADS for you, but it's really easy to do on your own via [mongodump](https://www.mongodb.com/download-center/community)
* Refer to our docs on [installing mongodb tools](docs/install-mongodb.md#extract-and-setup-mongodb-binaries)
* Implement `mongodump` to backup your database, we recommend using a git repository as it will take care of revisioning and updates for you.
* Below is an example script we use for this purpose, this assumes you have a git repository already setup you can push to with ssh access.

```
#!/bin/bash
# script to call mongodump and dump quads db, push to git.

backup_database() {
    mongodump --out /opt/quads/backups/
}

sync_git() {
    cd /opt/quads/backups
    git add quads/*
    git add admin/*
    git commit -m "$(date) content commit"
    git push
}

backup_database
sync_git
```

## Restoring QUADS DB from Backup
* If you have a valid mongodump directory structure you can restore the QUADS database via the following command.
* This will drop the current database and replace it with your mongodump copy

   - First, cd to the parent directory of where your mongorestore is kept

```
[root@host-04 rdu2-quads-backup-mongo]# ls

admin  mongodump  mongodump-quads.sh  quads  README.md
```

  - `quads` is the directory containing our database dump files

* Use mongorestore to drop the current quads database and replace with your backup

```
mongorestore --drop -d quads quads
```

  - You will see some messages and all should be good.

```
2019-05-05T01:23:01.257+0100	building a list of collections to restore from quads dir
2019-05-05T01:23:01.270+0100	reading metadata for quads.vlan from quads/vlan.metadata.json
2019-05-05T01:23:01.282+0100	reading metadata for quads.host from quads/host.metadata.json
2019-05-05T01:23:01.288+0100	reading metadata for quads.counters from quads/counters.metadata.json
2019-05-05T01:23:01.294+0100	reading metadata for quads.schedule from quads/schedule.metadata.json
2019-05-05T01:23:01.329+0100	restoring quads.vlan from quads/vlan.bson
2019-05-05T01:23:01.361+0100	restoring quads.host from quads/host.bson
2019-05-05T01:23:01.396+0100	restoring quads.counters from quads/counters.bson
2019-05-05T01:23:01.426+0100	restoring quads.schedule from quads/schedule.bson
2019-05-05T01:23:01.434+0100	restoring indexes for collection quads.vlan from metadata
2019-05-05T01:23:01.434+0100	restoring indexes for collection quads.host from metadata
2019-05-05T01:23:01.524+0100	finished restoring quads.host (494 documents)
2019-05-05T01:23:01.549+0100	finished restoring quads.vlan (148 documents)
2019-05-05T01:23:01.549+0100	reading metadata for quads.notification from quads/notification.metadata.json
2019-05-05T01:23:01.567+0100	reading metadata for quads.cloud_history from quads/cloud_history.metadata.json
2019-05-05T01:23:01.568+0100	no indexes to restore
2019-05-05T01:23:01.568+0100	finished restoring quads.counters (334 documents)
2019-05-05T01:23:01.602+0100	restoring quads.notification from quads/notification.bson
2019-05-05T01:23:01.643+0100	restoring quads.cloud_history from quads/cloud_history.bson
2019-05-05T01:23:01.659+0100	reading metadata for quads.cloud from quads/cloud.metadata.json
2019-05-05T01:23:01.661+0100	no indexes to restore
2019-05-05T01:23:01.661+0100	finished restoring quads.notification (41 documents)
2019-05-05T01:23:01.699+0100	restoring quads.cloud from quads/cloud.bson
2019-05-05T01:23:01.717+0100	restoring indexes for collection quads.cloud_history from metadata
2019-05-05T01:23:01.718+0100	no indexes to restore
2019-05-05T01:23:01.718+0100	finished restoring quads.schedule (433 documents)
2019-05-05T01:23:01.742+0100	restoring indexes for collection quads.cloud from metadata
2019-05-05T01:23:01.743+0100	finished restoring quads.cloud_history (94 documents)
2019-05-05T01:23:01.792+0100	finished restoring quads.cloud (32 documents)
2019-05-05T01:23:01.792+0100	done
```

## QUADS Talks and Media
[![Skynet your Infrastructure with QUADS @ EuroPython 2017](http://img.youtube.com/vi/9e1ZhtBliHc/0.jpg)](https://www.youtube.com/watch?v=9e1ZhtBliHc "Skynet your Infrastructure with QUADS")

   - [Skynet your Infrastructure with QUADS @ Europython 2017 Slides](https://hobosource.files.wordpress.com/2016/11/skynet_quads_europython_2017_wfoster.pdf)
   - [Skynet your Infrastructure with QUADS @ DevOps Pro Moscow 2018 Slides](https://hobosource.files.wordpress.com/2017/11/quads_devopspro_moscow_wfoster_2017-11-16.pdf)
