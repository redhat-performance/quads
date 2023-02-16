QUADS (quick and dirty scheduler)
=================================

QUADS automates the future scheduling, end-to-end provisioning and delivery of bare-metal servers and networks.

* Visit the [QUADS blog](https://quads.dev)
* Please read our [contributing guide](https://github.com/redhat-performance/quads/blob/master/CONTRIBUTING.md) and use [Gerrit Review](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) to submit patches.

![quads](/image/quads.jpg?raw=true)

![quads-rpm-build](https://copr.fedorainfracloud.org/coprs/quadsdev/python3-quads/package/quads/status_image/last_build.png)

   * [QUADS (quick and dirty scheduler)](#quads-quick-and-dirty-scheduler)
      * [What does it do?](#what-does-it-do)
      * [Design](#design)
      * [Requirements](#requirements)
      * [Setup Overview](#setup-overview)
      * [QUADS Workflow](#quads-workflow)
      * [QUADS Switch and Host Setup](#quads-switch-and-host-setup)
      * [Installing QUADS](#installing-quads)
         * [Installing QUADS from RPM](#installing-quads-from-rpm)
         * [Installing other QUADS Components](#installing-other-quads-components)
            * [QUADS Wiki](#quads-wiki)
               * [Installing Wordpress via Ansible](#installing-wordpress-via-ansible)
               * [Setup of Wordpress](#setup-of-wordpress)
               * [Limit Page Revisions in Wordpress](#limit-page-revisions-in-wordpress)
            * [QUADS Move Command](#quads-move-command)
         * [Making QUADS Run](#making-quads-run)
      * [QUADS Usage Documentation](#quads-usage-documentation)
         * [Adding New Hosts to QUADS](#adding-new-hosts-to-quads)
            * [Define Initial Cloud Environments](#define-initial-cloud-environments)
            * [Define Host in QUADS and Foreman](#define-host-in-quads-and-foreman)
            * [Define Host Interfaces in QUADS](#define-host-interfaces-in-quads)
         * [How Provisioning Works](#how-provisioning-works)
            * [QUADS Move Host Command](#quads-move-host-command)
      * [QUADS Reporting](#quads-reporting)
        * [Future Assignment Reporting](#future-assignment-reporting)
        * [Server Availability Overview Report](#server-availability-overview-report)
        * [Assignment Scheduling Statistics](#assignment-scheduling-statistics)
        * [Upcoming Scheduled Assignments Report](#upcoming-scheduled-assignments-report)
      * [Common Administration Tasks](#common-administration-tasks)
         * [Creating a New Cloud Assignment and Schedule](#creating-a-new-cloud-assignment-and-schedule)
            * [QUADS VLAN Options](#quads-vlan-options)
            * [Optional QUADS Public VLAN](#optional-quads-public-vlan)
            * [Defining a New Cloud](#defining-a-new-cloud)
            * [Adding New Hosts to your Cloud](#adding-new-hosts-to-your-cloud)
            * [Adding New Hosts to your Cloud with JIRA Integration](#adding-new-hosts-to-your-cloud-with-jira-integration)
         * [Managing Faulty Hosts](#managing-faulty-hosts)
            * [Migrating to QUADS-managed Host Health](#migrating-to-quads-managed-host-health)
         * [Managing Retired Hosts](#managing-retired-hosts)
         * [Extending the <strong>Schedule</strong> of an Existing Cloud](#extending-the-schedule-of-an-existing-cloud)
         * [Extending the <strong>Schedule</strong> of a Specific Host](#extending-the-schedule-of-a-specific-host)
         * [Shrinking the <strong>Schedule</strong> of an Existing Cloud](#shrinking-the-schedule-of-an-existing-cloud)
         * [Shrinking the <strong>Schedule</strong> of a Specific Host](#shrinking-the-schedule-of-a-specific-host)
         * [Terminating a <strong>Schedule</strong>](#terminating-a-schedule)
         * [Adding Hosts to an existing Cloud](#adding-hosts-to-an-existing-cloud)
         * [Removing a Schedule](#removing-a-schedule)
         * [Removing a Schedule across a large set of hosts](#removing-a-schedule-across-a-large-set-of-hosts)
         * [Removing a Host from QUADS](#removing-a-host-from-quads)
         * [Modify a Host Interface](#modify-a-host-interface)
         * [Remove a Host Interface](#remove-a-host-interface)
      * [Using the QUADS JSON API](#using-the-quads-json-api)
      * [Additional Tools and Commands](#additional-tools-and-commands)
         * [Verify or Correct Cloud and Host Network Switch Settings](#verify-or-correct-cloud-and-host-network-switch-settings)
         * [Modify or check a specific Host Network Switch Settings](#modify-or-check-a-specific-host-network-switch-settings)
            * [Mapping Interface to VLAN ID](#mapping-interface-to-vlan-id)
         * [Modifying Cloud-level Attributes](#modifying-cloud-level-attributes)
         * [Looking into the Future](#looking-into-the-future)
         * [Dry Run for Pending Actions](#dry-run-for-pending-actions)
         * [Find Free Cloud Environment](#find-free-cloud-environment)
         * [Find Available Hosts](#find-available-hosts)
            * [Find Available Hosts based on Hardware or Model](#find-available-hosts-based-on-hardware-or-model)
            * [Find Available Web Preview](#find-available-web-preview)
            * [Find a System by MAC Address](#find-a-system-by-mac-address)
            * [Find Systems by Switch IP Address](#find-systems-by-switch-ip-address)
      * [Interacting with MongoDB](#interacting-with-mongodb)
      * [Using JIRA with QUADS](#using-jira-with-quads)
      * [Backing up QUADS](#backing-up-quads)
      * [Restoring QUADS DB from Backup](#restoring-quads-db-from-backup)
      * [Troubleshooting Validation Failures](#troubleshooting-validation-failures)
         * [Understanding Validation Structure](#understanding-validation-structure)
         * [Troubleshooting Steps](#troubleshooting-steps)
         * [Validation using Debug Mode](#validation-using-debug-mode)
         * [Skipping Past Network Validation](#skipping-past-network-validation)
         * [Skipping Past Foreman Validation](#skipping-past-foreman-validation)
         * [Validate Only a Specific Cloud](#validate-only-a-specific-cloud)
         * [Mapping Internal VLAN Interfaces to Problem Hosts](#mapping-internal-vlan-interfaces-to-problem-hosts)
      * [Contact QUADS Developers](#contact-quads-developers)
      * [QUADS Talks and Media](#quads-talks-and-media)

## What does it do?
   - Create and manage unlimited future scheduling for automated slicing & dicing of systems and network infrastructure
   - Drive automated systems provisioning and network switch changes to deliver isolated, multi-tenant bare-metal environments
   - Automated network and provisioning validation prior to delivering sets of machines/networks to tenants
   - Automated allocation of optional, publicly routable VLANs
   - Generates/maintains user-configurable [instackenv.json](https://docs.openstack.org/tripleo-docs/latest/install/environments/baremetal.html#instackenv-json) to accomodate OpenStack deployment.
   - Generates/maintains user-configurable ocpinventory.json for OpenShift on Baremetal Deployments
   - Automatically generate/maintain documentation to illustrate current status, published to a [Wordpress instance](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html#pages)
     * Current system details, infrastructure fleet inventory
     * Current system group ownership (cloud), workloads and assignments
     * Total duration and time remaining in system assignments
     * Dynamic provisioning & system/network validation status per assignment
     * Currently allocated/free optional publicly routable VLAN status
   - Query scheduling data to determine future availability
   - Generates a per-month visualization map for per-machine allocations to assignments.
   - JIRA integration.
   - Webhook and IRC notifications (via supybot/notify plugin) for system releases.
   - Email notifications to users for new future assignments, releases and expirations.
   - Flask-based Web UI for searching for available bare-metal systems in the future based on model.

## Design
   - Main components: `Python3, CherryPy, Mongoengine, MongoDB, Jinja2`
   - Installation via RPM for Fedora Linux.
   - We use [Badfish](https://github.com/redhat-performance/badfish) for managing bare-metal IPMI
   - We use [Foreman](https://theforeman.org/) for the systems provisioning backend.
   - We use [Wordpress](https://wordpress.org/) for auto-generating wiki and documentation.
   - A typical container-based QUADS deployment might look like this:

![quadsarchitecture](/image/quads-container-architecture.png?raw=true)

## Requirements
   - In QUADS 1.1+ we are using Python3, Cherrypy and Jinja2 with MongoDB as the database backend.
   - The scheduling functionality can be used standalone, but you'll want a provisioning backend like [Foreman](https://theforeman.org/) to take full advantage of QUADS scheduling, automation and provisioning capabilities.
   - To utilize the automatic wiki/docs generation we use [Wordpress](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/) but anything that accepts markdown via an API should work.
   - Switch/VLAN automation is done on Juniper Switches in [Q-in-Q VLANs](http://www.jnpr.net/techpubs/en_US/junos14.1/topics/concept/qinq-tunneling-qfx-series.html), but command sets can easily be extended to support other network switch models.
   - We use [badfish](https://github.com/redhat-performance/badfish) for Dell systems to manage boot order to accomodate OpenStack deployments via Ironic/Triple-O as well as to control power actions via the Redfish API.

## Setup Overview
   - Documentation for setting up and using QUADS is available in detail within this repository.
   - Below is a high-level overview of a greenfield setup, some of this may exist already for you.

| Step | Documentation | Details |
|------|---------------|---------|
| General Architecture Overview | [docs](/docs/quads-workflow.md) | Architecture overview |
| Install and Setup Foreman/Satellite | [docs](https://theforeman.org/manuals/nightly/#3.InstallingForeman) | Not covered here |
| Setup Foreman/Satellite Validation Templates | [examples](/templates/README.md) | Templates for internal interface configs |
| Prepare Host and Network Environment | [docs](/docs/switch-host-setup.md) | Covers Juniper Environments, IPMI, Foreman |
| Install QUADS | [docs](#installing-quads) | Install via RPM |
| Install MongoDB | [docs](/docs/install-mongodb.md) | Install MongoDB separately |
| Install Wiki | [docs](#installing-wordpress-via-ansible) | Use Ansible to Deploy Wordpress |
| Configure Wiki | [docs](#setup-of-wordpress) | Configure Wordpress Pages and Plugins |
| Configure your QUADS Move Command | [docs](#quads-move-command) | Configure your provisioning and move actions |
| Configure QUADS Crons | [docs](#making-quads-run) |  Tell QUADS how to manage your infrastructure |
| Add Clouds and Hosts | [docs](#adding-new-hosts-to-quads) | Configure your hosts and environments in QUADS |
| Host Metadata Model and Search | [docs](/docs/quads-host-metadata-search.md) | Host metadata info and filtering |
| Using JIRA with QUADS | [docs](/docs/using-jira-with-quads.md) | Optional JIRA tools and library for QUADS |
## QUADS Workflow

You can read about QUADS architecture, provisioning, visuals and workflow [in our documentation examples and screenshots](/docs/quads-workflow.md)

## QUADS Switch and Host Setup
   - To ensure you have setup your network switches and bare-metal hosts properly please follow our [Switch and Host Setup Docs](/docs/switch-host-setup.md)

## Installing QUADS
   - We support modern Fedora OS distributions using RPM packages.
   - While we will provide Docker/container files this is more for CI testing and isn't recommended or properly maintained for production deployments.

### Installing QUADS from RPM
   - We build RPM packages for the Fedora distribution.
   - On Fedora 30 and above you'll need to manually install mongodb first, see [installing mongodb for QUADS](docs/install-mongodb.md)
   - On Fedora 30 and above it is necessary to install `python3-wordpress-xmlrpc` as it is not included anymore

```
rpm -ivh --nodeps https://funcamp.net/w/python3-wordpress-xmlrpc-2.3-14.noarch.rpm
```
This package is also available via `pip` via `pip install python-wordpress-xmlrpc`


* Once you have mongodb installed and running you can install/upgrade QUADS via RPM.

```
dnf copr enable quadsdev/python3-quads  -y
dnf install quads -y
```

* Note: If you want the latest development RPM based on the `master` branch instead:

```
dnf install quads-dev -y
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
   - The Wiki component for QUADS is currently Wordpress, though in 2.x we'll be moving everything to Flask.
   - Please use **Red Hat, CentOS Stream or Rocky 8** for the below Wordpress component.
   - Wordpress needs to be on it's **own VM/server** as a standalone component.
   - [Wordpress](https://github.com/redhat-performance/ops-tools/tree/master/ansible/wiki-wordpress-nginx-mariadb) provides a place to automate documentation and inventory/server status via the Wordpress Python RPC API.

##### Installing Wordpress via Ansible
   - You can use our Ansible playbook for installing Wordpress / PHP / PHP-FPM / nginx on a Rocky8, RHEL8 or CentOS8 Stream standalone virtual machine.
   - First, clone the repository
```
git clone https://github.com/redhat-performance/ops-tools
cd ansible/wiki-wordpress-nginx-mariadb
```
  - Second, add the hostname or IP address of your intended Wiki/Wordpress host replacing `wiki.example.com` with your host in the `hosts` file.
```
# cat hosts
[wordpress_server]
wiki.example.com
```
  - Third, run Ansible to deploy.  You might take a look at `group_vars/all` for any configuration settings you want to change first.
```
ansible-playbook -i hosts site.yml
```
##### Setup of Wordpress
   - You'll then simply need to create an `infrastructure` page and `assignments` page and denote their `page id` for use in automation.  This is set in `conf/quads.yml`
   - We also provide the [krusze theme](/docker/etc/wordpress/themes/krusze.0.9.7.zip) which does a great job of rendering Markdown-based tables, and the [JP Markdown plugin](/docker/etc/wordpress/plugins/jetpack-markdown.3.9.6.zip) which is required to upload Markdown to the [Wordpress XMLRPC Python API](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/).  The `Classic Editor` plugin is also useful.  All themes and plugins can be activated from settings.

##### Limit Page Revisions in Wordpress
   - It's advised to set the following parameter in your `wp-config.php` file to limit the amount of page revisions that are kept in the database.
     - Before the first reference to `ABSPATH` in `wp-config.php` add:

```
define('WP_POST_REVISIONS', 100);
```
   - You can always clear out your old page revisions via the `wp-cli` utility as well, QUADS regenerates all content as it changes so there is no need to keep around old revisions of pages unless you want to.

```
yum install wp-cli -y
su - wordpress -s /bin/bash
wp post delete --force $(wp post list --post_type='revision' --format=ids)
```
#### QUADS Move Command
   - QUADS relies on calling an external script, trigger or workflow to enact the actual provisioning of machines. You can look at and modify our [move-and-rebuild-hosts](https://github.com/redhat-performance/quads/blob/master/quads/tools/move_and_rebuild_hosts.py) tool to suit your environment for this purpose.  Read more about this in the [move-host-command](https://github.com/redhat-performance/quads#quads-move-host-command) section below.

   - Note: RPM installations will have ```quads-cli``` and tools in your system $PATH but you will need to login to a new shell to pick it up.

### Making QUADS Run
   - QUADS is a passive service and does not do anything you do not tell it to do.  We control QUADS with cron, please copy and modify our [example cron commands](https://raw.githubusercontent.com/redhat-performance/quads/master/cron/quads) to your liking, adjust as needed.

   - Below are the major components run out of cron that makes everything work.

| Service Command | Category | Purpose |
|-----------------|----------|---------|
| quads-cli --move-hosts | provisioning | checks for hosts to move/reclaim as scheduled |
| validate_env.py | validation | checks clouds pending to be released for all enabled validation checks |
| regenerate_wiki.py | documentation | keeps your infra wiki updated based on current state of environment |
| simple_table_web.py | visualization | keeps your systems availability and usage visualization up to date |
| make_instackenv_json.py | openstack | keeps optional openstack triple-o installation files up-to-date |


## QUADS Usage Documentation

### Adding New Hosts to QUADS

#### Define Initial Cloud Environments
   - Define the various cloud environments
   - These are the isolated environments QUADS will use and provision into for you.

```
quads-cli --define-cloud --cloud cloud01 --description "Primary Cloud Environment"
quads-cli --define-cloud --cloud cloud02 --description "02 Cloud Environment"
quads-cli --define-cloud --cloud cloud03 --description "03 Cloud Environment"
```

#### Define Host in QUADS and Foreman

   - Define the hosts in the environment (Foreman Example)
     - Note the ```--host-type``` parameter, this is a mandatory, free-form label that can be anything.  It will be used later for ```post-config``` automation and categorization.
     - If you don't want systems to be reprovisioned when they move into a cloud environment append `--no-wipe` to the define command.
     - We are excluding anything starting with mgmt- and including servers with the name r630.

```
for h in $(hammer host list --per-page 1000 | egrep -v "mgmt|c08-h30"| grep r630 | awk '{ print $3 }') ; do quads-cli --define-host $h --default-cloud cloud01 --host-type general; done
```

   - The command **without Foreman** would be simply:

```
quads-cli --define-host --host <hostname> --default-cloud cloud01 --host-type general
```

#### Define Host Interfaces in QUADS

   - Define the host interfaces, these are the internal interfaces you want QUADS to manage for VLAN automation
   - Do this for every interface you want QUADS to manage per host (we are working on auto-discovery of this step).
   - The variable `default_pxe_interface` on the quads.yml will set the default value of `pxe_boot=True` for that interface while any other interface will have a default value of `False` unless specified via `--pxe-boot` or `--no-pxe-boot`. This can be later modified via `--mod-interface`.

```
quads-cli --add-interface --interface-name em1 --interface-mac 52:54:00:d9:5d:df --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:0 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
quads-cli --add-interface --interface-name em2 --interface-mac 52:54:00:d9:5d:dg --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:1 --interface-vendor "Intel" --interface-speed 1000 --pxe-boot --host <hostname>
quads-cli --add-interface --interface-name em3 --interface-mac 52:54:00:d9:5d:dh --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:2 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
quads-cli --add-interface --interface-name em4 --interface-mac 52:54:00:d9:5d:d1 --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:3 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
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

{"name": "em1", "mac_address": "52:54:00:d9:5d:df", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:0"}
{"name": "em2", "mac_address": "52:54:00:d9:5d:dg", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:1"}
{"name": "em3", "mac_address": "52:54:00:d9:5d:dh", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:2"}
{"name": "em4", "mac_address": "52:54:00:d9:5d:d1", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:3"}
```

   - To see the current system allocations:

```
quads-cli --summary
```
```
cloud01 : 45 (Primary Cloud Environment)
cloud02 : 22 (02 Cloud Environment)
```
   - For a more detailed summary of current system allocations use `--detail`

```
quads-cli --summary --detail
```
```
cloud01 (quads): 45 (Primary Cloud Environment) - 451
cloud02 (jdoe): 22 (02 Cloud Environment) - 462
```
   - For including clouds with no active assignments use `--all`

```
quads-cli --summary --detail --all
```
```
cloud01 (quads): 45 (Primary Cloud Environment) - 451
cloud02 (jdoe): 22 (02 Cloud Environment) - 462
cloud03 (jhoffa): 0 (03 Cloud Environment) - 367
```
**NOTE:**

The format here is based on the following:
`{cloud_name} ({owner}): {count} ({description}) - {ticket_number}`

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
In QUADS, a `move-command` is the actionable call that provisions and moves a set of systems from one cloud environment to the other.  Via cron, QUADS routinely queries the existing schedules and when it comes time for a set of systems to move to a new environment or be reclaimed and moved back to the spare pool it will run the appropriate varation of your `move-command`.

In the above example the default move command called ```/bin/echo``` for illustration purposes.  In order for this to do something more meaningful you should invoke a script with the ```--move-command``` option, which should be the path to a valid command or provisioning script/workflow.

* Define your move command by pointing QUADS to an external command, trigger or script.
* This expects three arguments `hostname current-cloud new-cloud`.
* Runs against all hosts according to the QUADS schedule.

```
quads-cli --move-hosts --move-command quads/tools/move_and_rebuild_hosts.py
```

* You can modify the default settings via the `default_move_command` setting in [quads-cli](https://github.com/redhat-performance/quads/blob/master/bin/quads-cli).

* You can look at the [move-and-rebuild-hosts](https://github.com/redhat-performance/quads/blob/master/quads/tools/move_and_rebuild_hosts.py) script as an example.  It's useful to note that with `quads/tools/             move_and_rebuild_hosts.py` passing a fourth argument will result in only the network automation running and the actual host provisioning will be skipped.  You should review this script and adapt it to your needs, we try to make variables for everything but some assumptions are made to fit our running environments.

## QUADS Reporting

### Future Assignment Reporting

As of QUADS `1.1.6` we now have the `--report-detailed` command which will list all upcoming future assignments that are scheduled.
You can also specify custom start and end dates via `--schedule-start "YYYY-MM-DD HH:MM"` and `--schedule-stop "YYYY-MM-DD HH:MM"`

```
quads-cli --report-detailed
```
Example Output
```
Owner    |    Ticket|    Cloud| Description| Systems|  Scheduled| Duration|
tcruise  |      1034|  cloud20|   Openshift|       6| 2022-02-06|       14|
cwalken  |      1031|  cloud19|   Openstack|       6| 2022-02-06|       14|
bhicks   |      1029|  cloud18| Openstack-B|       4| 2022-02-06|       14|
nreeves  |      1028|  cloud11| Openshift-P|       2| 2022-02-06|       14|
gcarlin  |      1026|  cloud08|        Ceph|       4| 2022-02-06|       14|
```

### Server Availability Overview Report

Generate a report with a list of server types with total count of systems and their current and future availability plus an average build time delta overall

```
quads-cli --report-available
```
Example output
```
Quads report for 2019-12-01 to 2019-12-31:
Percentage Utilized: 60%
Average build delta: 0:00:26.703556
Server Type | Total|  Free| Scheduled| 2 weeks| 4 weeks
r620        |     5|     0|      100%|       0|       0
1029p       |     3|     3|        0%|       3|       3
```

Additionally, you can pass `--schedule-start` and `--schedule-end` dates for reports in the past. 2 weeks and 4 weeks free calculate starting days from the first Sunday following when the command was run, or return current day at 22:01 if run on Sunday.

### Assignment Scheduling Statistics

Generate a report detailing systems and scheduling utilization over the course of months or years.

```
quads-cli --report-scheduled --months 6
```
Example Output
```
Month   | Scheduled|  Systems|  % Utilized|
2022-02 |         1|     1268|         42%|
2022-01 |         9|     1268|         66%|
2022-02 |         1|     1268|         42%|
2021-09 |        10|     1226|         83%|
2021-08 |        14|     1215|         77%|
2021-07 |         3|     1215|         87%|
```

### Upcoming Scheduled Assignments Report

Generate statistics on the number of assigned clouds in quads over a period of months in the past starting today or on a specific year.

```
quads-cli --report-scheduled --months 6
```
Example output
```
Month   | Scheduled|  Systems|  % Utilized|
2019-12 |         0|        8|         58%|
2019-11 |         2|        8|         62%|
2019-10 |        15|        8|         20%|
2019-09 |         0|        0|          0%|
2019-08 |         0|        0|          0%|

```

Additionally, you can pass `--year` instead for a report for every month in that year.

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

This pertains to the internal interfaces that QUADS will manage for you to move sets of hosts between environments based on a schedule.  For setting up optional publicly routable VLANS please see the [QUADS public vlan setup steps](/docs/switch-host-setup.md#define-optional-public-vlans)

   -  VLAN design (optional, will default to `qinq: 0` below)

   - ```qinq: 0``` (default) qinq VLAN separation by interface: primary, secondary and beyond QUADS-managed interfaces all match the same VLAN membership across other hosts in the same cloud allocation.  Each interface per host is in its own VLAN, and these match across the rest of your allocated hosts by interface (all nic1, all nic2, all nic3, all nic4 etc).

   - ```qinq: 1``` all QUADS-managed interfaces in the same qinq VLAN. For this to take effect you need to pass the optional argument of `--qinq 1` to the `--define-cloud` command.

   - You can use the command `quads-cli --ls-qinq` to view your current assignment VLAN configuration:

```
quads-cli --ls-qinq
```
```
cloud01: 0 (Isolated)
cloud02: 1 (Combined)
cloud03: 0 (Isolated)
cloud04: 1 (Combined)
```

#### Optional QUADS Public VLAN ####

If you need to associate a public vlan (routable) with your cloud, quads currently supports associating your last NIC per host with one of your defined public VLANs (see the [QUADS public vlan setup steps](/docs/switch-host-setup.md#define-optional-public-vlans)).

To define your cloud with a public VLAN, use the following syntax:

```
quads-cli --define-cloud --cloud cloud03 [ other define-cloud options ] --vlan 601
```

If you need to clear the vlan association with your cloud, you can pass any string to the `--vlan` argument in `--mod-cloud`

```
quads-cli --mod-cloud --cloud cloud03 --vlan none
```

#### Defining a New Cloud ####

```
quads-cli --define-cloud --cloud cloud03 --description "Messaging AMQ" --force --cloud-owner epresley --cc-users "jdoe jhoffa" --cloud-ticket 423625 --qinq 1
```

   * Note: in QUADS `1.1.4` you can change any of these values selectively via the `--mod-cloud` command [described below](#modifying-cloud-level-attributes).

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

#### Adding New Hosts to your Cloud with JIRA Integration

   - **NOTE** If you are using [JIRA integration features](/docs/using-jira-with-quads.md) with QUADS 1.1.5 and higher you can utilize `--host-list` along with a list of hosts and it will take care of updating your `--cloud-ticket` in JIRA for you in one swoop.

```
quads-cli --add-schedule --host-list /tmp/hosts --schedule-start "2021-04-20 22:00" --schedule-end "2021-05-02 22:00" --schedule-cloud cloud20
```

That's it.  At this point your hosts will be queued for provision and move operations, we check once a minute if there are any pending provisioning tasks.  To check manually:

```
quads-cli --move-hosts --dry-run

```

After your hosts are provisioned and moved you should see them populate under the cloud list.

```
quads-cli --cloud-only cloud03
```

### Managing Faulty Hosts
Starting with `1.1.4` QUADS can manage broken or faulty hosts for you and ensure they are ommitted from being added to a future schedule or listed as available.  Prior to `1.1.4` this is managed via the Foreman host parameter `broken_state` (true/false).

* Listing all broken systems.
```
# quads-cli --ls-broken
f18-h22-000-r620.stage.example.com
```

* Marking a system as faulty
```
# quads-cli --mark-broken --host f18-h23-000-r620.example.com
Host f18-h23-000-r620.example.com is now marked as broken
```

* Marking a system as repaired or no longer faulty.
```
# quads-cli --mark-repaired --host f18-h23-000-r620.example.com
Host f18-h23-000-r620.example.com is now marked as repaired.
```

* Hosts marked as faulty will be ommitted from `--ls-available`
* Hosts marked as faulty are not able to be scheduled until they are marked as repaired again.

#### Migrating to QUADS-managed Host Health

* If you previously used the `broken_state` Foreman host parameter to manage your broken or out-of-service systems within your fleet you'll want to migrate to using the new methodology of the QUADS database handling this for you for versions `1.1.4` and higher.
* You can use the following command to query Foreman and convert `broken_state` host parameters and status into QUADS:

```
for h in $(hammer host list --per-page 1000 --search params.broken_state=true | grep $(egrep ^domain /opt/quads/conf/quads.yml | awk '{ print $NF }') | awk '{ print $3 }') ; do quads-cli --mark-broken --host $h ; done
```

### Managing Retired Hosts

* With QUADS `1.1.5` and higher we now have the `--retire`, `--unretire` and `--ls-retire` features to manage decomissioning or reviving hosts.
* Hosts marked as retired will still retain their scheduling history and data, but will not show as available unless filtered.
   - To list retired hosts:

```
quads-cli --ls-retire
```
* To retire a host:
```
quads-cli --retire --host host01.example.com
```
* To unretire a host:
```
quads-cli --unretire --host host01.example.com
```

* **NOTE** If upgrading from `1.1.4.1` or earlier QUADS you will need the following settings applied before using `--retire`.
* This can be referenced in the [changelog/release notes](https://github.com/redhat-performance/quads/releases/tag/v1.1.5) as well.

```
$ cd /opt/quads
$ python
>>> from quads.model import Host
>>> hosts = Host.objects()
>>> for host in hosts:
...	if not host.retired:
...		host.update(retired=False)
```

### Extending the __Schedule__ of an Existing Cloud

Occasionally you'll want to extend the lifetime of a particular assignment. QUADS lets you do this with one command but you'll want to double-check things first.
In this example we'll be extending the assignment end date for cloud02

In QUADS version `1.1.4` or higher or the current `master` branch you can extend a cloud environment with a simple command.

```
quads-cli --extend --cloud cloud02 --weeks 2 --check
```

This will check whether or not the environment can be extended without conflicts.

To go ahead and extend it remove the `--check`

```
quads-cli --extend --cloud cloud02 --weeks 2
```

### Extending the __Schedule__ of a Specific Host

You might also want to extend the lifetime of a specific host.
In this example we'll be extending the assignment end date for host01.

```
quads-cli --extend --host host01 --weeks 2 --check
```

This will check whether or not the environment can be extended without conflicts.

To go ahead and extend it remove the `--check`

```
quads-cli --extend --host host01 --weeks 2
```

### Shrinking the __Schedule__ of an Existing Cloud

Occasionally you'll want to shrink the lifetime of a particular assignment.
In this example we'll be shrinking the assignment end date for cloud02

```
quads-cli --shrink --cloud cloud02 --weeks 2 --check
```

This will check whether or not the environment can be shrunk without conflicts.

To go ahead and shrink it remove the `--check`

```
quads-cli --shrink --cloud cloud02 --weeks 2
```

### Shrinking the __Schedule__ of a Specific Host

You might also want to shrink the lifetime of a specific host.
In this example we'll be shrinking the assignment end date for host01.

```
quads-cli --shrink --host host01 --weeks 2 --check
```

This will check whether or not the host schedule can be shrunk without conflicts.

To go ahead and shrink it remove the `--check`

```
quads-cli --shrink --host host01 --weeks 2
```

### Terminating a __Schedule__

If you would like to terminate the lifetime of a schedule at either a host or cloud level, you can pass the `--now` argument instead of `--weeks` which will set the schedules end date to now.
In this example we'll be terminating the assignment end date for cloud02.

```
quads-cli --shrink --cloud cloud02 --now --check
```

This will check whether or not the environment can be terminated without conflicts.

To go ahead and terminate it remove the `--check`

```
quads-cli --shrink --cloud cloud02 --now
```

### Adding Hosts to an existing Cloud

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
quads-cli --rm-schedule --schedule-id 2 --host c08-h01-r930.rdu.openstack.example.com
quads-cli --rm-schedule --schedule-id 2 --host c08-h01-r930.rdu.openstack.example.com
quads-cli --rm-schedule --schedule-id 2 --host c08-h01-r930.rdu.openstack.example.com
```

### Removing a Schedule across a large set of hosts

You should search for either the start or end dates to select the right schedule ID to remove when performing schedule removals across a large set of hosts.

   - If you are using QUADS in any serious capacity **always pick this option**.
   - Example: removing schedule by searching for start date.
   - Often machine schedule ID's are different for the same schedule across a set of machines, this ensures you remove the right one.

```
for host in $(cat /tmp/452851); do quads-cli --rm-schedule --schedule-id $(quads-cli --ls-schedule --host $host | grep cloud08 | grep "start=2017-08-06" | tail -1 | awk -F\| '{ print $1 }') --host $host ; echo Done. ; done
```

### Removing a Host from QUADS

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```
quads-cli --rm-host f03-h30-000-r720xd.rdu2.example.com
Removed: {'host': 'f03-h30-000-r720xd.rdu2.example.com'}
```

### Modify a Host Interface

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```
quads-cli --mod-interface --interface-name em1 --host f03-h30-000-r720xd.rdu2.example.com --no-pxe-boot
Interface successfully updated
```

### Remove a Host Interface

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```
quads-cli --rm-interface --interface-name em1 --host f03-h30-000-r720xd.rdu2.example.com
Resource properly removed
```

## Using the QUADS JSON API
* All QUADS actions under the covers uses the JSON API v2
   - Please [read about the QUADS RESTful API here](/docs/quads-api.md)
* This is an optional local systemd service you can start and interact with and listens on localhost ```TCP/8080```

## Additional Tools and Commands

### Verify or Correct Cloud and Host Network Switch Settings
* The tool `/opt/quads/quads/verify_switchconf.py` can be used to both validate and correct network switch configs.
* This can be run at a cloud level (and with 1.1.5+ also at the per-host level).
* It's advised to run it first without `--change` to see if it would fix something.
* This will also check/correct optional routable VLANs if those are in use.
* To validate a clouds network config:

```
/opt/quads/quads/tools/verify_switchconf.py --cloud cloud10
```

* To validate and fix a clouds network config use `--change`

```
/opt/quads/quads/tools/verify_switchconf.py --cloud cloud10 --change
```

* To validate a singular hosts network switch configuration:
```
/opt/quads/quads/tools/verify_switchconf.py --host host01.example.com
```

* To validate and fix a single hosts network config use `--change`

```
/opt/quads/quads/tools/verify_switchconf.py --host host01.example.com --change
```

* To straddle clouds and place a single host into a cloud it does not belong in (rare use case):
```
/opt/quads/quads/tools/verify_switchconf.py --host host01.example.com --cloud cloud10
```

Note, if host01.example.com is not in cloud10, but rather cloud20, you will see the following output:
```
WARNING - Both --cloud and --host have been specified.
WARNING -
WARNING - Host: host01.example.com
WARNING - Cloud: cloud10
WARNING -
WARNING - However, host01.example.com is a member of cloud20
WARNING -
WARNING - !!!!! Be certain this is what you want to do. !!!!!
WARNING -
```

### Modify or check a specific Host Network Switch Settings
* With the `modify_switch_conf.py` tool you can set up each individual network interface to a specific vlan id.
* Passing the `--change` argument will make the changes effective in the switch. Not passing this will only verify the configuration is set to the desired.

```
/opt/quads/quads/tools/modify_switch_conf.py --host host01.example.com --nic1 1400 --nic2 1401 --nic3 1400 --nic4 1402 --nic5 1400
```
* All `--nic*` arguments are optional so this can be also done individually for all nics.

#### Mapping Interface to VLAN ID
* An easy way to figure out what VLAN corresponds to what generic `em` interface in the QUADS `--ls-interfaces` information we now include the following tool:
```
./opt/quads/quads/tools/ls_switch_conf.py --cloud cloud32
INFO - Cloud qinq: 1
INFO - Interface em1 appears to be a member of VLAN 1410
INFO - Interface em2 appears to be a member of VLAN 1410
```

This tool also accepts the `--all` argument which will list a detail for all hosts in the cloud.

Additional you can achieve the same with the following shell one-liner, setting `cloud=XX` for the cloud and adjusting `$(seq 1 4)` for your interface ranges available on the host.

```
cloud=32 ; origin=1100 ; offset=$(expr $(expr $cloud - 1) \* 10); vl=$(expr $origin + $offset) ;for i in $(seq 1 4) ; do vlan=$(expr $vl + $i - 1) ; echo "em$i is interface VLAN $vlan in cloud$cloud" ; done
```

```
em1 is interface VLAN 1400 in cloud32
em2 is interface VLAN 1401 in cloud32
em3 is interface VLAN 1402 in cloud32
em4 is interface VLAN 1403 in cloud32
```

* You can then use this information to map specific interfaces into other VLAN/clouds as required for more one-off or ad-hoc requirements beyond the standard VLAN modes that QUADS currently supports.
* **Note** that this would be an example for the default `Q-in-Q 0 (isolated)` VLAN configuration.  The `Q-in-Q 1 (combined)` configuration would simple be `VLAN1400` for all interfaces above respectively.


### Modifying Cloud-level Attributes
* You can redefine or change any aspects of an already-defined cloud starting in `1.1.4` with the `--mod-cloud` command.
* This can be done a per-parameter or combined basis:

```
quads-cli --mod-cloud --cloud cloud02 --cloud-owner jhoffa
```

```
quads-cli --mod-cloud --cloud cloud04 --cc-users "tpetty fmercury"
```

```
quads-cli --mod-cloud --cloud cloud06 --vlan 604 --wipe
```

```
quads-cli --mod-cloud --cloud cloud50 --no-wipe
```

```
quads-cli --mod-cloud --cloud cloud50 --vlan none
```

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

* The `--ls-available` functionality lets you search for available hosts in the future based on a date range or other criteria.

  - Find based on a date range:

```
quads-cli --ls-available --schedule-start "2019-12-05 08:00" --schedule-end "2019-12-15 08:00"
```

  - Find based on starting now with an end range:

```
quads --ls-available --schedule-end "2019-06-02 22:00"
```

#### Find Available Hosts based on Hardware or Model

* In QUADS `1.1.4` and higher you can now filter your availability search based on hardware capabilities or model type.
* Using this feature requires [importing hardware metadata](/docs/quads-host-metadata-search.md#how-to-import-host-metadata)
* Example below using `--filter "model==1029U-TRTP"`

```
quads-cli --ls-available --schedule-start "2020-08-02 22:00" --schedule-end "2020-08-16 22:00" --filter "model==1029U-TRTP"
```

* Listing retired hosts can now use the `--filter` feature:

```
quads-cli --ls-hosts --filter "retired==True"
```

* Listing specific hosts from a certain cloud:

```
quads-cli --cloud-only --cloud cloud13 --filter "model==FC640"
```

#### Find Available Web Interface

* We now have a Flask-based `--ls-available` web interface available on `quadshost:5001` if your firewall rules are open for `TCP/5001`.
* Available in QUADS `1.1.4` or above as a tech preview (when we migrate fully to Flask this will be supplanted with a full UI).
* This is provided via the `quads-web` systemd service or you can run it manually via `cd /opt/quads/web ; python3 main.py`
* You will need to seed the `models` data for your systems using the new [host metadata feature](/docs/quads-host-metadata-search.md)

![quads-available-web](/image/quads-available-web.png?raw=true)

* Control + click can select more than one model
* Not selecting a model assumes a search for anything available.

#### Find a System by MAC Address
* You can utilize the new metadata model and `--filter` command in `1.1.4` and above along with `--ls-hosts` to search for a system by MAC Address.

```
quads-cli --ls-hosts --filter "interfaces.mac_address==ac:1f:6b:2d:19:48"
```

#### Find Systems by Switch IP Address
* You can list what systems are connected to a switch by querying the `ip_address` (soon to be `switch_ip` in 1.1.7) information from the interfaces datasource.

```
quads-cli --ls-hosts --filter "interfaces.ip_address==10.1.34.210"
```

## Interacting with MongoDB
* In some scenarios you may wish to interrogate or modify values within MongoDB.  You should be careful doing this and have good backups in place.  Generally, we will try to implement data, object and document modification needs through quads-cli so you don't need to do this but sometimes it's useful for troubleshooting or other reasons.

   - For more information see [Interacting with MongoDB](/docs/interact-mongodb.md)

## Using JIRA with QUADS
* We utilize the JIRA ticketing system internally for R&D infrastructure requests managed by QUADS.
* We do provide some best-effort tooling and a JIRA library to bridge automation gaps.

   - For more information see [Using JIRA with QUADS](/docs/using-jira-with-quads.md)

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

## Troubleshooting Validation Failures
A useful part of QUADS is the functionality for automated systems/network validation.  Below you'll find some steps to help understand why systems/networks might not pass validation so you can address any issues.

### Understanding Validation Structure
There are two main validation tests that occur before a cloud environment is automatically released:

* **Foreman Systems Validation** ensures that no target systems in your environment are marked for build.
* **VLAN Network Validation** ensures that all the backend interfaces in your isolated VLANs are reachable via fping

All of these validations are run from `/opt/quads/quads/tools/validate_env.py` and we also ship a few useful tools to help you figure out validation failures.

`/opt/quads/quads/tools/validate_env.py` is run from cron, see our [example cron entry](cron/quads)

### Troubleshooting Steps
You should run through each of these steps manually to determine what systems/networks might need attention of automated validation does not pass in a reasonable timeframe.  Typically, `admin_cc:` will receieve email notifications of trouble hosts as well.


* **General Availability** can be checked via a simple `fping` command, this should be run first.

```
quads-cli --cloud-only cloud23 > /tmp/cloud23
fping -u -f /tmp/cloud23
```

* **Foreman Systems Validation** can be run via the hammer cli command provided by `gem install hammer_cli_foreman_admin hammer_cli`

```
for host in $(quads-cli --cloud-only cloud15) ; do echo $host $(hammer host info --name $host | grep -i build); done
```

No systems should be left marked for build.

### Validation using Debug Mode
* **NOTE** Automated validation **will not** start until 2 hours after the assignment is scheduled to go out, until this point `/opt/quads/quads/tools/validate_env.py` will not attempt to validate any systems if run and they have started less than 2 hours ago.
  - This can be set via the `validation_grace_period:` setting in `/opt/quads/conf/quads.yml`

* `/opt/quads/quads/tools/validate_env.py` now has a `--debug` option which tells you what's happening during validation.
* This will test the backend network connectivity part and the entire set of checks.

* **Successful Validation** looks like this:

```
/opt/quads/quads/tools/validate_env.py --debug
```

```
Validating cloud23
Using selector: EpollSelector
:Initializing Foreman object:
GET: /status
GET: /hosts?search=build=true
Command executed successfully: fping -u f12-h01-000-1029u.rdu2.scalelab.example.com f12-h02-000-1029u.rdu2.scalelab.example.com f12-h03-000-1029u.rdu2.scalelab.example.com
Command executed successfully: fping -u 172.16.38.126 172.20.38.126 172.16.36.206
Command executed successfully: fping -u 172.17.38.126 172.21.38.126 172.17.36.206
Command executed successfully: fping -u 172.18.38.126 172.22.38.126 172.18.36.206
Command executed successfully: fping -u 172.19.38.126 172.23.38.126 172.19.36.206
Subject: Validation check succeeded for cloud23
From: RDU2 Scale Lab <quads@example.com>
To: dev-null@example.com
Cc: wfoster@example.com, kambiz@example.com, jtaleric@example.com,
 abond@example.com, grafuls@example.com, natashba@example.com
Reply-To: dev-null@example.com
User-Agent: Rufus Postman 1.0.99
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0

A post allocation check previously failed for:

   cloud: cloud23
   owner: ipinto
   ticket: 498569

has successfully passed the verification test(s)!  The owner
should receive a notification that the environment is ready
for use.

DevOps Team

 cloud23 / ipinto / 498569
```

* **Unsuccessful Validation** looks like this:

```
/opt/quads/quads/tools/validate_env.py --debug
```

```
Validating cloud23
Using selector: EpollSelector
:Initializing Foreman object:
GET: /status
GET: /hosts?search=build=true
There was something wrong with your request
ICMP Host Unreachable from 10.1.38.126 for ICMP Echo sent to f12-h14-000-1029u.rdu2.scalelab.example.com (10.1.38.43)

ICMP Host Unreachable from 10.1.38.126 for ICMP Echo sent to f12-h14-000-1029u.rdu2.scalelab.example.com (10.1.38.43)

ICMP Host Unreachable from 10.1.38.126 for ICMP Echo sent to f12-h14-000-1029u.rdu2.scalelab.example.com (10.1.38.43)

ICMP Host Unreachable from 10.1.38.126 for ICMP Echo sent to f12-h14-000-1029u.rdu2.scalelab.example.com (10.1.38.43)
```

### Skipping Past Network Validation

* In `QUADS 1.1.6+` you can skip past network validation via:

```
/opt/quads/tools/validate_env.py --skip-network
```

* In older versions of QUADS you will want to consult the documentation for [interacting with MongoDB](/docs/interact-mongodb.md) for how to override this check.

### Skipping Past Foreman Validation

* If you know your systems are built you can force `validate_env.py` to move into the network portions of the validation by toggling the `provisioned` attribute in MongoDB for your cloud object.

```
db.cloud.update({"name": "cloud23"}, {$set:{'provisioned':true}}
```

* More information on manual intervention and overrides via MongoDB can be [found here](/docs/interact-mongodb.md)

### Validate Only a Specific Cloud

* If you want to validate only a certain cloud you can do so by specifying the cloud's name with the `--cloud` flag.
```bash
/opt/quads/tools/validate_env.py --cloud cloud01
```

### Mapping Internal VLAN Interfaces to Problem Hosts
You might have noticed that we configure our [Foreman](https://github.com/redhat-performance/quads/tree/master/templates/foreman) templates to drop `172.{16,17,18,19}.x` internal VLAN interfaces which correspond to the internal, QUADS-managed multi-tenant interfaces across a set of hosts in a cloud assignment.

The _first two octets_ here can be substituted by the _first two octets of your systems public network_ in order to determine from `validate_env.py --debug` which host internal interfaces have issues or are unreachable.

![validation_1](/image/troubleshoot_validation1.png?raw=true)

* Above, we can run the `host` command to determine what these machines map to by substituting `10.1` for the first two octects:

```
# for host in 10.1.37.231 10.1.38.150; do host $host; done
231.37.1.10.in-addr.arpa domain name pointer e17-h26-b04-fc640.example.com.
150.38.1.10.in-addr.arpa domain name pointer e17-h26-b03-fc640.example.com.
```

* Below you can see the code that maintains this mapping and assumptions:

![validation_2](/image/troubleshoot_validation2.png?raw=true)

This mapping feeds into our [VLAN network validation code](https://github.com/redhat-performance/quads/blob/master/quads/tools/validate_env.py#L143)

## Contact QUADS Developers

Besides Github we're also on IRC via `irc.libera.chat`.  You can [click here](https://web.libera.chat/?channels=#quads) to join in your browser.

## QUADS Talks and Media
[![Skynet your Infrastructure with QUADS @ EuroPython 2017](http://img.youtube.com/vi/9e1ZhtBliHc/0.jpg)](https://www.youtube.com/watch?v=9e1ZhtBliHc "Skynet your Infrastructure with QUADS")

   - [Skynet your Infrastructure with QUADS @ Europython 2017 Slides](https://hobosource.files.wordpress.com/2016/11/skynet_quads_europython_2017_wfoster.pdf)
   - [Skynet your Infrastructure with QUADS @ DevOps Pro Moscow 2018 Slides](https://hobosource.files.wordpress.com/2017/11/quads_devopspro_moscow_wfoster_2017-11-16.pdf)
