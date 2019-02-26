QUADS (quick and dirty scheduler)
====================================

Automate scheduling and end-to-end provisioning of servers and networks.

* Please read our [contributing guide](https://github.com/redhat-performance/quads/blob/master/CONTRIBUTING.md) and use [Gerrit Review](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) to submit patches.
* [Waffle.io](https://waffle.io/redhat-performance/quads) is also available for additional development tracking and priorities.

![quads](/image/quads.jpg?raw=true)


![quads-rpm-build](https://copr.fedorainfracloud.org/coprs/quadsdev/python3-quads/package/quads/status_image/last_build.png)

   * [QUADS (quick and dirty scheduler)](#quads-quick-and-dirty-scheduler)
      * [What does it do?](#what-does-it-do)
      * [Design](#design)
      * [Requirements](#requirements)
      * [QUADS Workflow](#quads-workflow)
      * [QUADS Switch and Host Setup](#quads-switch-and-host-setup)
      * [Installing QUADS](#installing-quads)
         * [Installing QUADS with Docker Compose (Recommended)](#installing-quads-with-docker-compose-recommended)
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
         * [Extending the <strong>Schedule</strong> of Existing Cloud with Differing
           Active Schedules](#extending-the-schedule-of-existing-cloud-with-differing-active-schedules)
         * [Extending Machine Allocation to an existing Cloud](#extending-machine-allocation-to-an-existing-cloud)
         * [Removing a Schedule](#removing-a-schedule)
         * [Removing a Schedule across a large set of hosts](#removing-a-schedule-across-a-large-set-of-hosts)
      * [Additional Tools and Commands](#additional-tools-and-commands)
      * [Using the QUADS JSON API](#using-the-quads-json-api)
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
   - Main components: `Python3, Cherrypy, MongoDB, Jinja2`
   - Installation via Docker compose, RPM (Fedora or EL8+) or Github sources
   - We use [badfish](https://github.com/redhat-performance/badfish) for managing bare-metal IPMI
   - We use [Foreman](https://theforeman.org/) for the systems provisioning backend.

## Requirements
   - In QUADS 1.1+ we are using Python3, Cherrypy and Jinja2 with MongoDB as the database backend.
   - The scheduling functionality can be used standalone, but you'll want a provisioning backend like [Foreman](https://theforeman.org/) to take full advantage of QUADS scheduling, automation and provisioning capabilities.
   - To utilize the automatic wiki/docs generation we use [Wordpress](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/) but anything that accepts markdown via an API should work.
   - Switch/VLAN automation is done on Juniper Switches in [Q-in-Q VLANs](http://www.jnpr.net/techpubs/en_US/junos14.1/topics/concept/qinq-tunneling-qfx-series.html), but commandsets can easily be extended to support other network switch models.
   - We use [badfish](https://github.com/redhat-performance/badfish) for optional Dell playbooks to toggle boot order and PXE flags to accomodate OpenStack deployments via Ironic/Triple-O.
   - The package [ansible-cmdb](https://github.com/fboender/ansible-cmdb) needs to be available if you want to see per assignment Ansible facts of the inventory. It can be obtained from [here](https://github.com/fboender/ansible-cmdb/releases)

## QUADS Workflow

You can read about QUADS mechanics, provisioning, visuals and workflow [in our documentation examples and screenshots](/docs/quads-workflow.md)

## QUADS Switch and Host Setup
   - To ensure you have setup your switch properly please follow our [Switch and Host Setup Docs](/docs/switch-host-setup.md)

## Installing QUADS
   - We offer Docker compose, RPM packages or a Git clone installation (for non RPM-based distributions, BSD UNIX, etc).
   - It's recommended to use the Docker method as it requires less setup.

### Installing QUADS with Docker Compose *(Recommended)*
   - Clone the QUADS Github repository
```
git clone --single-branch --branch master https://github.com/redhat-performance/quads /opt/docker/quads
```
   - Read through the [QUADS YAML configuration file](/conf/quads.yml) for other settings you way want.
```
vi /opt/docker/quads/conf/quads.yml
```
   - Run docker-compose to instantiate a full QUADS stack
```
docker-compose -f /opt/docker/quads/docker/docker-compose.yml up -d
```
   - Access Quads Wiki via browser at `http://localhost`
   - Run commands against containerized quads via docker exec

```
docker exec quads bin/quads-cli --define-cloud cloud01 --description cloud01
```

We find it useful to create an alias on your quads container for executing quads-cli commands inside the container.

   - On your docker host:
```
echo 'alias quads="docker exec -it quads bin/quads-cli"' >> ~/.bashrc
```

### Installing QUADS from Github
   - Clone the git repository (substitute paths below as needed)

```
git clone https://github.com/redhat-performance/quads /opt/quads
```
   - Install pre-requisite Python packages
```
yum install expectk python3-aexpect python-requests
```
   - Install a webserver (Apache, nginx, etc)
```
yum install httpd
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
   - Note: You can use QUADS on non-systemd based Linux or UNIX distributions but you'll need to run ```/opt/quads/bin/quads-server``` via an alternative init process or similiar (It's just a Python HTTP application).

### Installing QUADS from RPM
   - On Fedora *(and eventually CentOS/RHEL 8+ when it's available)*

```
dnf copr enable quadsdev/python3-quads  -y
dnf install quads -y
```
   - Read through the [QUADS YAML configuration file](/conf/quads.yml)
```
vi /opt/quads/conf/quads.yml
```
   - Enable and start the QUADS systemd service (daemon)
   - Note: You can change QUADS ```quads_base_url``` listening port in ```conf/quads.yml``` and use the ```--port``` option
```
systemctl enable quads-server.service
systemctl start quads-server.service
```
   - For full functionality with Foreman you'll also need to have [hammer cli](https://theforeman.org/2013/11/hammer-cli-for-foreman-part-i-setup.html) installed and setup on your QUADS host.

   - Note: RPM installations will have ```quads-cli``` and tools in your system $PATH but you will need to login to a new shell to pick it up.  We typically place this as an alias in `/root/.bashrc`.
```
echo 'alias quads="/opt/quads/bin/quads-cli"' >> /root/.bashrc
```

### Installing other QUADS Components
#### QUADS Wiki
   - There is also a Wordpress Wiki [VM](https://github.com/redhat-performance/ops-tools/tree/master/ansible/wiki-wordpress-nginx-mariadb) QUADS component that we use a place to automate documentation via a Markdown to Python RPC API but any Markdown-friendly documentation platform could suffice.
   - You'll then simply need to create an `infrastructure` page and `assignments` page and denote their `page id` for use in automation.  This is set in `conf/quads.yml`
   - We also provide the `krusze` theme which does a great job of rendering Markdown-based tables, and the `JP Markdown` plugin which is required to upload Markdown to the [Wordpress XMLRPC Python API](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/)
      * This will be containerized and documented in the near future via [GitHub Issue #102](https://github.com/redhat-performance/quads/issues/102)
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
/opt/quads/bin/quads-cli --define-cloud cloud01 --description "Primary Cloud Environment"
/opt/quads/bin/quads-cli --define-cloud cloud02 --description "02 Cloud Environment"
/opt/quads/bin/quads-cli --define-cloud cloud03 --description "03 Cloud Environment"
```

   - Define the hosts in the environment (Foreman Example)
     - Note the ```--host-type``` parameter, this is a mandatory, free-form label that can be anything.  It will be used later for ```post-config``` automation and categorization.
     - We are excluding anything starting with mgmt- and including servers with the name r630.

```
for h in $(hammer host list --per-page 1000 | egrep -v "mgmt|c08-h30"| grep r630 | awk '{ print $3 }') ; do /opt/quads/bin/quads-cli --define-host $h --default-cloud cloud01 --host-type general; done
```

   - The command without Foreman would be simply:

```
/opt/quads/bin/quads-cli --define-host <hostname> --default-cloud cloud01 --host-type general
```
   - To list the hosts:

```
/opt/quads/bin/quads-cli --ls-hosts
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

   - To see the current system allocations:

```
/opt/quads/bin/quads-cli --summary
```
```
cloud01 : 45 (Primary Cloud Environment)
cloud02 : 0 (02 Cloud Environment)
cloud03 : 0 (03 Cloud Environment)
```
   - Define a custom schedule for a host
     - Example: assign host ```c08-h21``` to the workload/cloud ```cloud02```

```
/opt/quads/bin/quads-cli --add-schedule --host c08-h21-r630.example.com --schedule-start "2016-07-11 08:00" --schedule-end "2016-07-12 08:00" --schedule-cloud cloud02
```

   - List the schedule for a specific host:

```
/opt/quads/bin/quads-cli --ls-schedule --host c08-h21-r630.example.com
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
/opt/quads/bin/quads-cli --move-hosts
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
/opt/quads/bin/quads-cli --move-hosts --path-to-command /opt/quads/bin/move-and-rebuild-host.sh
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
/opt/quads/bin/quads-cli --define-cloud cloud03 --description "Messaging AMQ" --force --cloud-owner epresley --cc-users "jdoe jhoffa" --cloud-ticket 423625 --qinq 0
```

   - Now that you've defined your new cloud you'll want to allocate machines and a schedule.
     - We're going to find the first 20 Dell r620's and assign them as an example.

#### Adding New Hosts to your Cloud ####
```
/opt/quads/bin/quads-cli --cloud-only cloud01 | grep r620 | head -20 > /tmp/RT423624
```

   - Now we'll allocate all of these hosts with a schedule, by default our system times use UTC.

```
for h in $(cat /tmp/RT423624) ; do /opt/quads/bin/quads-cli --host $h --add-schedule --schedule-start "2016-10-17 00:00" --schedule-end "2016-11-14 17:00" --schedule-cloud cloud03 ; done
```

That's it.  At this point your hosts will be queued for provision and move operations, we check once a minute if there are any pending provisioning tasks.  To check manually:

```
for h in $(./quads-cli  --cloud-only cloud03) ; do echo -n ==== $h   :" " ; cat /etc/lab/state/$h ; done
```

After your hosts are provisioned and moved you should see them populate under the cloud list.

```
/opt/quads/bin/quads-cli --cloud-only cloud03
```

### Extending the __Schedule__ of an Existing Cloud

Occasionally you'll want to extend the lifetime of a particular assignment. QUADS lets you do this with one command but you'll want to double-check things first.
In this example we'll be extending the assignment end date for cloud03

   - First, get the updated list of current assignments

```
/opt/quads/bin/quads-cli --summary
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
/opt/quads/bin/quads-cli --ls-owner
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
/opt/quads/bin/quads-cli --cloud-only cloud03
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
/opt/quads/bin/quads-cli --host b09-h01-r620.rdu.openstack.example.com --ls-schedule
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
for h in $(/opt/quads/bin/quads-cli --cloud-only cloud03) ; do /opt/quads/bin/quads-cli --host $h --mod-schedule 0 --schedule-end "2016-11-27 18:00"; done
```

  - Cleanup Notification Files

Your tenant may have already been receiving email notifications about machines coming up for reclamation, we want to clear these out so future notifications are up to date.
On the QUADS host you'll want to remove these files if they exist, in this case they will be called ```cloud03-jhoffa-$notifyday-$ticketid```

```
rm: remove regular empty file '/etc/lab/report/cloud03-jhoffa-5-423624'? y
rm: remove regular empty file '/etc/lab/report/cloud03-jhoffa-7-423624'? y
```

### Extending the __Schedule__ of Existing Cloud with Differing Active Schedules

When in heavy usage some machines primary, active schedule may differ from one another, e.g. 0 versus 1, versus 2, etc.  Because schedules operate on a per-host basis sometimes the same schedule used within a cloud may differ in schedule number.  Here's how you modify them across the board for the current active schedule if the ID differs.

* Example: extend all machines in cloud10 to end on 2016-01-09 05:00 UTC, these have differing primary active schedule IDs.

  - Check your commands via echo first
  - **Approach: 1** Modify the latest assignment

```
for h in $(/opt/quads/bin/quads-cli --cloud-only cloud10) ; do echo /opt/quads/bin/quads-cli --mod-schedule $(/opt/quads/bin/quads-cli --ls-schedule --host $h | grep "urrent s" | awk -F: '{ print $2 }') --host $h --schedule-end "2017-01-09 05:00" ; echo Done. ; done
```

Note the difference in commands needed with the ```--mod-schedule``` flag that is required.

```
/opt/quads/bin/quads-cli --mod-schedule 0 --host b10-h11-r620.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
/opt/quads/bin/quads-cli --mod-schedule 3 --host c08-h21-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
/opt/quads/bin/quads-cli --mod-schedule 3 --host c08-h22-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
/opt/quads/bin/quads-cli --mod-schedule 2 --host c08-h23-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
```

  - **Approach: 2** Reschedule against a certain cloud **and** start date **(RECOMMENDED)**

```
for h in $(/opt/quads/bin/quads-cli --cloud-only cloud05); do echo /opt/quads/bin/quads-cli --mod-schedule $(/opt/quads/bin/quads-cli --ls-schedule --host $h | grep cloud05 | grep "start=2017-02-09" | tail -1 | awk -F\| '{ print $1 }') --host $h --schedule-start "2017-02-09 05:00" --schedule-end "2017-03-06 05:00" ; echo Done. ; done
```

  * If all looks good you can remove **remove the echo lines** and apply.

### Extending Machine Allocation to an existing Cloud

QUADS also supports adding new machines into an existing workload (cloud).

   - Search Availability Pool for Free Servers
      - Let's look for any 5 x servers for 10 days

```
bin/find-available.py -c 5 -d 10
```
```
================
First available date = 2016-12-05 08:00
Requested end date = 2016-12-15 08:00
hostnames =
c03-h11-r620.rdu.openstack.example.com
c03-h13-r620.rdu.openstack.example.com
c03-h14-r620.rdu.openstack.example.com
c03-h15-r620.rdu.openstack.example.com
c03-h17-r620.rdu.openstack.example.com
```

  - Move New Hosts into Existing Cloud

Above we see all the free servers during our timeframe, let's move them into cloud10

```
/opt/quads/bin/quads-cli --host c03-h11-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
/opt/quads/bin/quads-cli --host c03-h13-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
/opt/quads/bin/quads-cli --host c03-h14-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
/opt/quads/bin/quads-cli --host c03-h15-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
/opt/quads/bin/quads-cli --host c03-h17-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
```

* Note: You can run ```bin/find-available-py``` with the ```--cli``` flag to generate QUADS commands for you.

### Removing a Schedule

You can remove an existing schedule across a set of hosts using the ```--rm-schedule``` flag against the schedule ID for each particular machine of that assignment.

   - Example: removing the schedule for three machines in cloud
   - Obtain the schedule ID via ```/opt/quads/bin/quads-cli --ls-schedule --host```
   - These machines would happen to have the same cloud assignment as schedule id 2.
```
/opt/quads/bin/quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
/opt/quads/bin/quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
/opt/quads/bin/quads-cli --rm-schedule 2 --host c08-h01-r930.rdu.openstack.example.com
```

### Removing a Schedule across a large set of hosts

You should search for either the start or end dates to select the right schedule ID to remove when performing schedule removals across a large set of hosts.

   - If you are using QUADS in any serious capacity **always pick this option**.
   - Example: removing schedule by searching for start date.
   - Often machine schedule ID's are different for the same schedule across a set of machines, this ensures you remove the right one.

```
for host in $(cat /tmp/452851); do /opt/quads/bin/quads-cli --rm-schedule $(/opt/quads/bin/quads-cli --ls-schedule --host $host | grep cloud08 | grep "start=2017-08-06" | tail -1 | awk -F\| '{ print $1 }') --host $host ; echo Done. ; done
```

## Using the QUADS JSON API
* All QUADS actions under the covers uses the JSON API v2
   - Please [read about the QUADS RESTful API here](/docs/quads-api.md)
* This is an optional local systemd service you can start and interact with and listens on localhost ```TCP/8080```

## Additional Tools and Commands

* You can display the allocation schedule on any given date via the ```--date``` flag.

```
/opt/quads/bin/quads-cli --date "2017-03-06"
```
```
cloud01:
  - b09-h01-r620.rdu.openstack.engineering.example.com
  - b09-h02-r620.rdu.openstack.engineering.example.com
  - b09-h03-r620.rdu.openstack.engineering.example.com
  - b09-h05-r620.rdu.openstack.engineering.example.com
  - b09-h06-r620.rdu.openstack.engineering.example.com
```

* You can use ```find-free-cloud.py``` to search for available clouds to assign new systems into for future assignments.

```
/opt/quads/bin/find-free-cloud.py
```

* You can see what's in progress or set to provision via the ```--dry-run``` sub-flag of ```--move-hosts```

```
/opt/quads/bin/quads-cli --move-hosts --dry-run
```
```
INFO: Moving b10-h27-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h18-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h19-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h21-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h25-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h26-r620.rdu.openstack.example.com from cloud01 to cloud03
```

* You can query all upcoming changes pending and what hosts are involved via the ```quads-change-list.sh``` tool.

```
/opt/quads/bin/quads-change-list.sh
```
```
Next change in 3 days
2016-12-22 05:00
INFO: Moving c01-h01-r620.rdu.openstack.example.com from cloud04 to cloud08
INFO: Moving c01-h02-r620.rdu.openstack.example.com from cloud04 to cloud08
INFO: Moving c01-h03-r620.rdu.openstack.example.com from cloud04 to cloud08
INFO: Moving c01-h05-r620.rdu.openstack.example.com from cloud04 to cloud08
INFO: Moving c01-h06-r620.rdu.openstack.example.com from cloud04 to cloud08
```

* When managing notification recipients you can use the ```--ls-cc-users``` and ```--cc-users``` arguments.

```
/opt/quads/bin/quads-cli --ls-cc-users --cloud-only cloud04
```
```
epresley
```
   - To add or remove recipients they need to be added or removed with space separation and you'll need to redefine the cloud definition.
   - Get a list of all the atributes and redefine

```
/opt/quads/bin/quads-cli --full-summary | grep cloud04 ; /opt/quads/bin/quads-cli --ls-owner | grep cloud04 ; /opt/quads/bin/quads-cli --ls-ticket | grep cloud04 ; /opt/quads/bin/quads-cli --ls-cc-users --cloud-only cloud04
```
```
cloud04 : 52 (Ceph deployment)
cloud04 : jhoffa
cloud04 : 423424
epresley
```
   - Redefine

```
/opt/quads/bin/quads-cli --define-cloud cloud04 --description "Ceph Deployment" --force --cloud-owner jhoffa --cc-users "epresley rnixon" --cloud-ticket 423424
```
   - Now you can see the updated cc notifications

```
/opt/quads/bin/quads-cli --ls-cc-users --cloud-only cloud04
```
```
epresley
rnixon
```

## QUADS Talks and Media
[![Skynet your Infrastructure with QUADS @ EuroPython 2017](http://img.youtube.com/vi/9e1ZhtBliHc/0.jpg)](https://www.youtube.com/watch?v=9e1ZhtBliHc "Skynet your Infrastructure with QUADS")

   - [Skynet your Infrastructure with QUADS @ Europython 2017 Slides](https://hobosource.files.wordpress.com/2016/11/skynet_quads_europython_2017_wfoster.pdf)
   - [Skynet your Infrastructure with QUADS @ DevOps Pro Moscow 2018 Slides](https://hobosource.files.wordpress.com/2017/11/quads_devopspro_moscow_wfoster_2017-11-16.pdf)
