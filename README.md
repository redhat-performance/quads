QUADS (quick and dirty scheduler)
=================================
![quads](/image/quads.png)

QUADS automates the future scheduling, end-to-end provisioning and delivery of bare-metal servers and networks.

* Visit the [QUADS blog](https://quads.dev)
* Please read our [contributing guide](https://github.com/redhat-performance/quads/blob/latest/CONTRIBUTING.md) and use [Gerrit Review](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) to submit patches.


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
            * [Using SSL with Flask API and QUADS](#using-ssl-with-flask-api-and-quads)
         * [QUADS Wiki](#quads-wiki)
            * [Dynamic Wiki Content](#dynamic-wiki-content)
              * [Ordering Dynamic Wiki Content](#ordering-elements-in-the-dynamic-wiki-content)
         * [Installing other QUADS Components](#installing-other-quads-components)
            * [QUADS Move Command](#quads-move-command)
         * [Making QUADS Run](#making-quads-run)
            * [Major Components](#major-components)
            * [External Services](#external-services)
      * [QUADS Usage Documentation](#quads-usage-documentation)
         * [Adding New Hosts to QUADS](#adding-new-hosts-to-quads)
            * [Define Initial Cloud Environments](#define-initial-cloud-environments)
            * [Define Host in QUADS and Foreman](#define-host-in-quads-and-foreman)
              * [Define your Server Models](#define-your-server-models)
              * [Define your QUADS Hosts](#define-your-quads-hosts)
            * [Define Host Interfaces in QUADS](#define-host-interfaces-in-quads)
         * [How Provisioning Works](#how-provisioning-works)
            * [QUADS Move Host Command](#quads-move-host-command)
      * [QUADS Reporting](#quads-reporting)
        * [Future Assignment Reporting](#future-assignment-reporting)
        * [Server Availability Overview Report](#server-availability-overview-report)
        * [Assignment Scheduling Statistics](#assignment-scheduling-statistics)
        * [Upcoming Scheduled Assignments Report](#upcoming-scheduled-assignments-report)
      * [Customizing Environment Web Details](#customizing-environment-web-details)
        * [Changing the Default Lab Name](#changing-the-default-lab-name)
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
            * [Retiring Hosts](#retiring-hosts)
         * [Extending the <strong>Schedule</strong> of an Existing Cloud](#extending-the-schedule-of-an-existing-cloud)
         * [Extending the <strong>Schedule</strong> of a Specific Host](#extending-the-schedule-of-a-specific-host)
         * [Shrinking the <strong>Schedule</strong> of an Existing Cloud](#shrinking-the-schedule-of-an-existing-cloud)
         * [Shrinking the <strong>Schedule</strong> of a Specific Host](#shrinking-the-schedule-of-a-specific-host)
         * [Terminating a <strong>Schedule</strong>](#terminating-a-schedule)
         * [Adding Hosts to an existing Cloud](#adding-hosts-to-an-existing-cloud)
         * [Removing a Schedule](#removing-a-schedule)
         * [Removing a Schedule across a large set of hosts](#removing-a-schedule-across-a-large-set-of-hosts)
         * [Removing a Host from QUADS](#removing-a-host-from-quads)
         * [Modifying a Host Schedule](#modifying-a-host-schedule)
            * [Modifying a Host Schedule across a large set of hosts](#modifying-a-host-schedule-across-a-large-set-of-hosts)
         * [Modify a Host Interface](#modify-a-host-interface)
         * [Remove a Host Interface](#remove-a-host-interface)
      * [Using the QUADS JSON API](#using-the-quads-json-api)
      * [Filtering Systems by Hardware Capability](#filtering-systems-by-hardware-capability)
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
            * [Find Available Web Interface](#find-available-web-interface)
            * [Find a System by MAC Address](#find-a-system-by-mac-address)
            * [Find Systems by Switch IP Address](#find-systems-by-switch-ip-address)
      * [Using JIRA with QUADS](#using-jira-with-quads)
      * [Backing up QUADS](#backing-up-quads)
      * [Restoring QUADS from Backup](#restoring-quads-from-backup)
      * [Troubleshooting Validation Failures](#troubleshooting-validation-failures)
         * [Understanding Validation Structure](#understanding-validation-structure)
         * [Troubleshooting Steps](#troubleshooting-steps)
         * [Validation using Debug Mode](#validation-using-debug-mode)
         * [Skipping Past Network Validation](#skipping-past-network-validation)
         * [Skipping Past Host and Systems Validation](#skipping-past-host-and-systems-validation)
         * [Skipping Past Network and Systems Validation per Host](#skipping-past-network-and-systems-validation-per-host)
         * [Validate Only a Specific Cloud](#validate-only-a-specific-cloud)
         * [Mapping Internal VLAN Interfaces to Problem Hosts](#mapping-internal-vlan-interfaces-to-problem-hosts)
         * [Validating after Removing Hosts](#validating-after-removing-hosts)
      * [Contact QUADS Developers](#contact-quads-developers)
      * [QUADS Talks and Media](#quads-talks-and-media)

## What does it do?
   - Create and manage unlimited future scheduling for automated slicing & dicing of systems and network infrastructure
   - Drive automated systems provisioning and network switch changes to deliver isolated, multi-tenant bare-metal environments
   - Automated network and provisioning validation prior to delivering sets of machines/networks to tenants
   - Automated allocation of optional, publicly routable VLANs
   - Generates/maintains user-configurable [instackenv.json](https://docs.openstack.org/tripleo-docs/latest/install/environments/baremetal.html#instackenv-json) to accomodate OpenStack deployment.
   - Generates/maintains user-configurable ocpinventory.json for OpenShift on Baremetal Deployments
   - Automatically generate/maintain documentation to illustrate current status
     * Current system details, infrastructure fleet inventory
     * Current system group ownership (cloud), workloads and assignments
     * Total duration and time remaining in system assignments
     * Dynamic provisioning & system/network validation status per assignment
     * Currently allocated/free optional publicly routable VLAN status
   - Query scheduling data to determine future availability
   - Generates a per-month visualization map for per-machine allocations to assignments.
   - JIRA integration.
   - Chat webhook and IRC notifications (via supybot/notify plugin) for system releases.
   - Email notifications to users for new future assignments, releases and expirations.
   - Flask-based Web UI for searching for available bare-metal systems in the future based on model.
   - Open, RESTful JSON API and RBAC for controlling access

## Design
   - Main components: `Python3, Flask, SqlAlchemy, PostrgreSQL, Jinja2`
   - Installation via RPM for Fedora Linux.
   - We use [Badfish](https://github.com/redhat-performance/badfish) for managing bare-metal IPMI
   - We use [Foreman](https://theforeman.org/) for the systems provisioning backend.
   - A typical QUADS deployment might look like this:

![quadsarchitecture](/image/quads-architecture.jpg)

## Requirements
   - Recent [Fedora Server](https://fedoraproject.org/server/download/) for RPM installations
   - 1 x modest sized VM for QUADS and the associated Wiki component
   - The scheduling functionality can be used standalone, but you'll want a provisioning backend like [Foreman](https://theforeman.org/) to take full advantage of QUADS scheduling, automation and provisioning capabilities.
   - Switch/VLAN automation is done on Juniper Switches in [Q-in-Q VLANs](http://www.jnpr.net/techpubs/en_US/junos14.1/topics/concept/qinq-tunneling-qfx-series.html), but command sets can easily be extended to support other network switch models.
   - We use [badfish](https://github.com/redhat-performance/badfish) for Dell systems to manage boot order to accomodate OpenStack deployments via Ironic/Triple-O as well as to control power actions via the Redfish API.

## Setup Overview
   - Documentation for setting up and using QUADS is available in detail within this repository.
   - Below is a high-level overview of a greenfield setup, some of this may exist already for you.

| Step | Documentation | Details |
|------|---------------|---------|
| General Architecture Overview | [docs](/docs/quads-workflow.md) | Architecture overview |
| Install and Setup Foreman/Satellite | [docs](https://theforeman.org/manuals/nightly/#3.InstallingForeman) | Not covered here |
| Setup Foreman/Satellite Validation Templates | [examples](/templates) | Templates for internal interface configs |
| Prepare Host and Network Environment | [docs](/docs/switch-host-setup.md) | Covers Juniper Environments, IPMI, Foreman |
| Install QUADS | [docs](#installing-quads) | Install via RPM |
| Enable SSL | [docs](#using-ssl-with-flask-api-and-quads) | Optionally enable SSL for API, Web |
| Configure your QUADS Move Command | [docs](#quads-move-command) | Configure your provisioning and move actions |
| Configure QUADS Crons | [docs](#making-quads-run) |  Tell QUADS how to manage your infrastructure |
| Add Clouds and Hosts | [docs](#adding-new-hosts-to-quads) | Configure your hosts and environments in QUADS |
| Host Metadata Model and Search | [docs](/docs/quads-host-metadata-search.md) | Host metadata info and filtering |
| Using the JSON API | [docs](/quads-api.md) | Interacting with the RESTful JSON API |
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
   - The following commands will install the QUADS package and all dependencies.

```bash
dnf copr enable quadsdev/python3-quads  -y
dnf install quads -y
```

   - Make sure the QUADS services are initialized via systemd:

```bash
systemctl start quads-{db,server,web}
```

   - Additionally, the `quads-db` needs to be initialized via the following command:

```bash
flask --app quads.server.app init-db
```

   - Now you're ready to go and start configuring QUADS environments, hosts, and other components below.
   - You should be able to access `quads-web` here now: http://QUADSVM and your [QUADS API](docs/quads-api.md) will also be available.
   - Make sure you open up TCP/80 and/or TCP/443 on your host firewall of choice, to enable SSL/TLS follow the next optional section.

#### Using SSL with Flask API and QUADS

This step is optional but may be welcoming due to recent HSTS enforcement in most browsers.

To enable TLS/SSL on QUADS (API, Web) you'll need to generate your own certificates, if you're cool with self-signed cerificates you can use this one-liner:

```
servername=$(hostname)
mkdir -p /etc/pki/tls/certs ; cd /etc/pki/tls/certs
openssl req -x509 -newkey rsa:4096 -keyout $servername.key -out $servername.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"
```

This generates your certificate and key here:

| SSL Component | File System Path                    |
| --------------|-------------------------------------|
| Nginx Cert    | /etc/pki/tls/certs/servername.pem   |
| Nginx Key     | /etc/pki/tls/certs/servername.key   |


Next you'll need to copy `apiv3_ssl.conf.example` into place as `apiv3_ssl.conf`

```
cd /etc/nginx/conf.d
cp apiv3_ssl.conf.example apiv3_ssl.conf
```

Lastly, in-line edit the configuration file to point to your generated cert/key pair.

```
servername=$(hostname) ; sed -i -e "s/quads.example.com/$servername/" /etc/nginx/conf.d/apiv3_ssl.conf
```

Lastly, restart nginx:

```
systemctl restart nginx
```

### QUADS Wiki
   - The Wiki component for QUADS is fully managed by `quads-web`

#### Dynamic Wiki Content
   - Additional content can be added dynamically to the wiki by adding content to the `/opt/quads/web` directory.
   - The way directory is to be structured is so that any directory is considered as a submenu of the `quads-web` navigation bar with the exception of `static` directories which are ignored by the navbar generation and which contain any static files for all the html files.
   - Additionally, the "friendly" text on the links will match that of the file without undescores.
   - Any files without extensions will be considered direct links with the content of it being only the hyperlink in plain text.
   - The html files should be structured for the correct jinja templating that is expected like this:

```
    {% extends "base.html" %}
    {% block title %} INSERT TITLE HERE {% endblock %}

    {% block page_content %}
    INSERT HTML CONTENT HERE
    {% endblock %}
```

   - For static files such as images and css, all files go on the root `/static` directory and the src href has to be passed via `url_for` like this:

```
        <img
          loading="lazy"
          decoding="async"
          class="alignnone size-full wp-image-5616"
          src="{{url_for('content.static', filename='scale_lab_assignments-march-may.png')}}"
          alt=""
          width="1030"
          height="542"
        />
```

##### Ordering Elements in the Dynamic Wiki Content
   - The type of content in the `/opt/quads/web` directory are either files or directories.
   - Flat files are either html files which follow the jinja templating, or direct links files which contain a link to an external resource.
   - Directories are translated into sub-menus and in turn can contain flat files as described above.
   - In order to control the ordering of various elements, they can be named with numeric prefixes.
   - Custom flat file elements are listed first, followed by sub-menu (Directory) elements.
   - Example of unnumbered content is as follows.  In this example, you will have a menu that contains `Chat`, `Contact`, `FAQ`, and `Usage`, followed by the Submenus `Docs`, `Resources` and `Tickets`

![Unordered Content](/image/Menus-Unnumbered.png)

   - If you wish to order them, rename your files and directories and add integer prefixes.  For example, the following will list the numbered elements followed by the un-numbered elements and would yield: `FAQ`, `Usage`, `Chat`, `Contact`, followed by the Submenus `Tickets`, `Resources` and `Docs` in that order.

![Ordered Content](/image/Menus-Numbered.png)



### Installing other QUADS Components

#### QUADS Move Command
   - QUADS relies on calling an external script, trigger or workflow to enact the actual provisioning of machines. You can look at and modify our [move-and-rebuild-hosts](https://github.com/redhat-performance/quads/blob/latest/src/quads/tools/move_and_rebuild.py) tool to suit your environment for this purpose.  Read more about this in the [move-host-command](https://github.com/redhat-performance/quads#quads-move-host-command) section below.

### Making QUADS Run
   - QUADS is a passive service and does not do anything you do not tell it to do.  We control QUADS with [cron commands](https://raw.githubusercontent.com/redhat-performance/quads/latest/cron/quads).
   - We ship an example cron file and install it for you that should work out of the box, it just has entries commented out.
   - To enable QUADS services to run you'll need to **uncomment them**.

```
crontab -e
```

#### Major Components

   - Below are the major components run out of cron that makes everything work.

| Service Command       | Category | Purpose |
|-----------------------|----------|---------|
| quads --move-hosts    | provisioning | checks for hosts to move/reclaim as scheduled |
| quads --validate-env  | validation | checks clouds pending to be released for all enabled validation checks |
| quads --regen-wiki    | documentation | keeps your infra wiki updated based on current state of environment |
| quads --regen-heatmap | visualization | keeps your systems availability and usage visualization up to date |
| quads --regen-instack | openshift/openstack | keeps optional openstack triple-o installation files up-to-date |
| quads --notify        | notifications | check and send email or webhook/IRC notifications on events and releases |

#### External Services

   - Really just the Foreman RBAC tool is needed for bare functionality, though there are a number of tools for JIRA automation that we ship in the repository as well that might be useful.

| Service Command       | Category | Purpose |
|-----------------------|----------|---------|
| quads --foreman-rbac  | RBAC | ensures environment user ownership maps to systems in Foreman |


## QUADS Usage Documentation

### Adding New Hosts to QUADS

#### Define Initial Cloud Environments
   - Define the various cloud environments
   - These are the isolated environments QUADS will use and provision into for you.
   - Note that **cloud01** is the designated "Spare Pool" where servers will go when they are first added and also when they have no active assignments to move to for a workload.  You can name it [anything you want](https://github.com/redhat-performance/quads/blob/latest/conf/quads.yml#L7) by editing the QUADS configuration file `/opt/quads/conf/quads.yml`

```bash
quads --define-cloud --cloud cloud01
quads --define-cloud --cloud cloud02 --description "02 Cloud Environment"
quads --define-cloud --cloud cloud03 --description "03 Cloud Environment"
```

#### Define Host in QUADS and Foreman

##### Define your Server Models

* Look for the `models:` [key/value pair](https://github.com/redhat-performance/quads/blob/latest/conf/quads.yml#L184) and add ones that accurately describe your fleet.
* This can be any identifiable string, we have added some stock ones we use for example but anything that makes sense to you to distinguish system models, sub-models etc that works for your needs e.g. R750-IL-XG might be a sub-model of a Dell R750.
* Models are used for filtering search, availability and other useful features and it's a mandatory data element you need to provide.


```
vi /opt/quads/conf/quads.yml
```

```
models: R620,R630,R640,R650,R930,R730XD,FC640
```

Now save this file and restart the QUADS server daemon.

```
systemctl restart quads-server
```

You will need to do this when you introduce new system models into your fleet if they are new.

##### Define your QUADS Hosts

   - Define the hosts in the environment (Foreman Example)
     - Note the ```--host-type``` parameter, this is a mandatory, free-form label that can be anything.  It will be used later for ```post-config``` automation and categorization.
     - If you don't want systems to be reprovisioned when they move into a cloud environment append `--no-wipe` to the define command.
     - We are excluding anything starting with mgmt- and including servers with the name r630.
     - Note that you **must define the model(s) of systems before you define them** in the previous step.

```bash
for h in $(hammer host list --per-page 1000 | egrep -v "mgmt|c08-h30"| grep r630 | awk '{ print $3 }') ; do quads --define-host $h --default-cloud cloud01 --host-type general --model R630; done
```

   - The command **without Foreman** would be simply:

```bash
quads --define-host --host <hostname> --default-cloud cloud01 --host-type general --model R630
```

#### Define Host Interfaces in QUADS

   - Define the host interfaces, these are the internal interfaces you want QUADS to manage for VLAN automation
   - Do this for every interface you want QUADS to manage per host (we are working on auto-discovery of this step).
   - The variable `default_pxe_interface` on the quads.yml will set the default value of `pxe_boot=True` for that interface while any other interface will have a default value of `False` unless specified via `--pxe-boot` or `--no-pxe-boot`. This can be later modified via `--mod-interface`.

```bash
quads --add-interface --interface-name em1 --interface-mac 52:54:00:d9:5d:df --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:0 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
quads --add-interface --interface-name em2 --interface-mac 52:54:00:d9:5d:dg --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:1 --interface-vendor "Intel" --interface-speed 1000 --pxe-boot --host <hostname>
quads --add-interface --interface-name em3 --interface-mac 52:54:00:d9:5d:dh --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:2 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
quads --add-interface --interface-name em4 --interface-mac 52:54:00:d9:5d:d1 --interface-switch-ip 10.12.22.201 --interface-port xe-0/0/1:3 --interface-vendor "Intel" --interface-speed 1000 --host <hostname>
```

   - To list the hosts:

```bash
quads --ls-hosts
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

```bash
quads --ls-interface --host c08-h21-r630.example.com

{"name": "em1", "mac_address": "52:54:00:d9:5d:df", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:0"}
{"name": "em2", "mac_address": "52:54:00:d9:5d:dg", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:1"}
{"name": "em3", "mac_address": "52:54:00:d9:5d:dh", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:2"}
{"name": "em4", "mac_address": "52:54:00:d9:5d:d1", "switch_ip": "10.12.22.201", "switch_port": "xe-0/0/1:3"}
```

   - To see the current system allocations:

```bash
quads --summary
```
```
cloud01 : 45 (Primary Cloud Environment)
cloud02 : 22 (02 Cloud Environment)
```
   - For a more detailed summary of current system allocations use `--detail`

```bash
quads --summary --detail
```
```
cloud01 (quads): 45 (Primary Cloud Environment) - 451
cloud02 (jdoe): 22 (02 Cloud Environment) - 462
```
   - For including clouds with no active assignments use `--all`

```bash
quads --summary --detail --all
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

```bash
quads --add-schedule --host c08-h21-r630.example.com --schedule-start "2016-07-11 08:00" --schedule-end "2016-07-12 08:00" --schedule-cloud cloud02
```

   - List the schedule for a specific host:

```bash
quads --ls-schedule --host c08-h21-r630.example.com
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

```bash
quads --move-hosts
```

You should see the following verbosity from a move operation

```
INFO: Moving c08-h21-r630.example.com from cloud01 to cloud02 c08-h21-r630.example.com cloud01 cloud02
```

### How Provisioning Works
#### QUADS move host command
In QUADS, a `move-command` is the actionable call that provisions and moves a set of systems from one cloud environment to the other.  Via cron, QUADS routinely queries the existing schedules and when it comes time for a set of systems to move to a new environment or be reclaimed and moved back to the spare pool it will run the appropriate varation of your `move-command`.

In the above example the default move command called ```/bin/echo``` for illustration purposes.  In order for this to do something more meaningful you should invoke a script with the ```--move-command``` option, which should be the path to a valid command or provisioning script/workflow.

* Define your move command by pointing QUADS to an external command, trigger or script if not using ours.
* This expects three arguments `hostname current-cloud new-cloud`.
* Runs against all hosts according to the QUADS schedule.

```bash
quads --move-hosts --move-command quads/tools/move_and_rebuild_hosts.py
```

* You can also modify the default `move_command` in [quads](https://github.com/redhat-performance/quads/blob/latest/src/quads/cli/cli.py#L31).

* You can look at the [move-and-rebuild-hosts](https://github.com/redhat-performance/quads/blob/latest/src/quads/tools/move_and_rebuild.py) tool as an example.  It's useful to note that with `move_and_rebuild.py` passing a fourth argument will result in only the network automation running and the actual host provisioning will be skipped.  You should review this script and adapt it to your needs, we try to make variables for everything but some assumptions are made to fit our running environments.

## QUADS Reporting

### Future Assignment Reporting

As of QUADS `1.1.6` we now have the `--report-detailed` command which will list all upcoming future assignments that are scheduled.
You can also specify custom start and end dates via `--schedule-start "YYYY-MM-DD HH:MM"` and `--schedule-stop "YYYY-MM-DD HH:MM"`

```bash
quads --report-detailed
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

```bash
quads --report-available
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

```bash
quads --report-scheduled --months 6
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

```bash
quads --report-scheduled --months 6
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

## Customizing Environment Web Details
### Changing the Default Lab Name
Until [this RFE](https://github.com/redhat-performance/quads/issues/537) is completed you'll need to change your lab name, or what you want to call your QUADS-managed environment in two separate `quads-web` files:

* Edit the [inventory.html](https://github.com/redhat-performance/quads/blob/latest/src/quads/web/templates/wiki/inventory.html#L5)
* Edit the [navbar.html](https://github.com/redhat-performance/quads/blob/latest/src/quads/web/templates/navbar.html#L2)

Restart `quads-web` to take effect.

```
systemctl restart quads-web
```

## Common Administration Tasks

### Creating a New Cloud Assignment and Schedule

Creating a new schedule and assigning machines is currently done through the QUADS CLI.  There are a few options you'll want to utilize.  Mandatory options are in bold and optional are in italics.

   -  **description** (this will appear on the assignments dynamic wiki)
   -  **cloud-owner** (for associating ownership and usage notifications)
   -  *force* (needed for re-using an existing cloud)
   -  *cc-users* (Add additional people to notifications, comma-separated)
   -  *cloud-ticket* (RT ticket used for the work, also appears in the assignments dynamic wiki)
   -  *wipe* (whether to reprovision machines going into this cloud, default is 1 or wipe.

#### QUADS VLAN Options

This pertains to the internal interfaces that QUADS will manage for you to move sets of hosts between environments based on a schedule.  For setting up optional publicly routable VLANS please see the [QUADS public vlan setup steps](/docs/switch-host-setup.md#define-optional-public-vlans)

   -  VLAN design (optional, will default to `qinq: 0` below)

   - ```qinq: 0``` (default) qinq VLAN separation by interface: primary, secondary and beyond QUADS-managed interfaces all match the same VLAN membership across other hosts in the same cloud allocation.  Each interface per host is in its own VLAN, and these match across the rest of your allocated hosts by interface (all nic1, all nic2, all nic3, all nic4 etc).

   - ```qinq: 1``` all QUADS-managed interfaces in the same qinq VLAN. For this to take effect you need to pass the optional argument of `--qinq 1` to the `--define-cloud` command.

   - You can use the command `quads --ls-qinq` to view your current assignment VLAN configuration:

```bash
quads --ls-qinq
```
```
cloud01: 0 (Isolated)
cloud02: 1 (Combined)
cloud03: 0 (Isolated)
cloud04: 1 (Combined)
```

#### Optional QUADS Public VLAN

If you need to associate a public vlan (routable) with your cloud, quads currently supports associating your last NIC per host with one of your defined public VLANs (see the [QUADS public vlan setup steps](/docs/switch-host-setup.md#define-optional-public-vlans)).

To define your cloud with a public VLAN, use the following syntax:

```bash
quads --define-cloud --cloud cloud03 [ other define-cloud options ] --vlan 601
```

If you need to clear the vlan association with your cloud, you can pass any string to the `--vlan` argument in `--mod-cloud`

```bash
quads --mod-cloud --cloud cloud03 --vlan none
```

#### Defining a New Cloud

```bash
quads --define-cloud --cloud cloud03 --description "Messaging AMQ" --cloud-owner epresley --cc-users "jdoe, jhoffa" --cloud-ticket 423625 --qinq 1
```

   * Note: in QUADS `1.1.4` you can change any of these values selectively via the `--mod-cloud` command [described below](#modifying-cloud-level-attributes).
   * Note: in QUADS `2.0` the `--force` command is no longer needed for defining inactive environments future use.

   - Now that you've defined your new cloud you'll want to allocate machines and a schedule.
     - We're going to find the first 20 Dell r620's and assign them as an example.

#### Adding New Hosts to your Cloud
```bash
quads --cloud-only --cloud cloud01 | grep r620 | head -20 > /tmp/RT423624
```
   - Now we'll allocate all of these hosts with a schedule, by default our system times use UTC.

```bash
quads --host-list /tmp/RT423624 --add-schedule --schedule-start "2016-10-17 00:00" --schedule-end "2016-11-14 17:00" --schedule-cloud cloud03
```

#### Adding New Hosts to your Cloud with JIRA Integration

   - **NOTE** If you are using [JIRA integration features](/docs/using-jira-with-quads.md) with QUADS 1.1.5 and higher you can utilize `--host-list` along with a list of hosts and it will take care of updating your `--cloud-ticket` in JIRA for you in one swoop.

```bash
quads --add-schedule --host-list /tmp/hosts --schedule-start "2021-04-20 22:00" --schedule-end "2021-05-02 22:00" --schedule-cloud cloud20
```

That's it.  At this point your hosts will be queued for provision and move operations, we check once a minute if there are any pending provisioning tasks.  To check manually:

```bash
quads --move-hosts --dry-run

```

After your hosts are provisioned and moved you should see them populate under the cloud list.

```bash
quads --cloud-only --cloud cloud03
```

### Managing Faulty Hosts
Starting with `1.1.4` QUADS can manage broken or faulty hosts for you and ensure they are ommitted from being added to a future schedule or listed as available.  Prior to `1.1.4` this is managed via the Foreman host parameter `broken_state` (true/false).

* Listing all broken systems.
```bash
# quads --ls-broken
f18-h22-000-r620.stage.example.com
```

* Marking a system as faulty
```bash
# quads --mark-broken --host f18-h23-000-r620.example.com
Host f18-h23-000-r620.example.com is now marked as broken
```

* Marking a system as repaired or no longer faulty.
```bash
# quads --mark-repaired --host f18-h23-000-r620.example.com
Host f18-h23-000-r620.example.com is now marked as repaired.
```

* Hosts marked as faulty will be ommitted from `--ls-available`
* Hosts marked as faulty are not able to be scheduled until they are marked as repaired again.

#### Migrating to QUADS-managed Host Health

* If you previously used the `broken_state` Foreman host parameter to manage your broken or out-of-service systems within your fleet you'll want to migrate to using the new methodology of the QUADS database handling this for you for versions `1.1.4` and higher.
* You can use the following command to query Foreman and convert `broken_state` host parameters and status into QUADS:

```bash
for h in $(hammer host list --per-page 1000 --search params.broken_state=true | grep $(egrep ^domain /opt/quads/conf/quads.yml | awk '{ print $NF }') | awk '{ print $3 }') ; do quads --mark-broken --host $h ; done
```

### Managing Retired Hosts

* With QUADS `1.1.5` and higher we now have the `--retire`, `--unretire` and `--ls-retire` features to manage decomissioning or reviving hosts.
* Hosts marked as retired will still retain their scheduling history and data, but will not show as available unless filtered.
   - To list retired hosts:

```bash
quads --ls-retire
```
* To retire a host:
```bash
quads --retire --host host01.example.com
```
* To unretire a host:
```bash
quads --unretire --host host01.example.com
```

#### Retiring Hosts
* Before retiring a host you should move it back to your resource pool first, in our case this is `cloud01`.
* This requires shrinking any active schedules on the host.
* The below command will shrink any active schedules on those hosts without prompting to terminate immediately.

```bash
for host in $(cat /tmp/retired_hosts); do yes | quads --shrink --host $host --now; done
```

* After this the defined `--move-host` command will want to move these back to your resource pool and power them off.
* `retired` hosts will remain officially in your resource pool but not show up in any visualizations or usage reporting, however their past usage history will all be available for record keeping and data requirements.

### Extending the Schedule of an Existing Cloud

Occasionally you'll want to extend the lifetime of a particular assignment. QUADS lets you do this with one command but you'll want to double-check things first.
In this example we'll be extending the assignment end date for cloud02

In QUADS version `1.1.4` or higher or the current `latest` branch you can extend a cloud environment with a simple command.

```bash
quads --extend --cloud cloud02 --weeks 2 --check
```

This will check whether or not the environment can be extended without conflicts.

To go ahead and extend it remove the `--check`

```bash
quads --extend --cloud cloud02 --weeks 2
```

### Extending the Schedule of a Specific Host

You might also want to extend the lifetime of a specific host.
In this example we'll be extending the assignment end date for host01.

```bash
quads --extend --host host01 --weeks 2 --check
```

This will check whether or not the environment can be extended without conflicts.

To go ahead and extend it remove the `--check`

```bash
quads --extend --host host01 --weeks 2
```

### Shrinking the Schedule of an Existing Cloud

Occasionally you'll want to shrink the lifetime of a particular assignment.
In this example we'll be shrinking the assignment end date for cloud02

```bash
quads --shrink --cloud cloud02 --weeks 2 --check
```

This will check whether or not the environment can be shrunk without conflicts.

To go ahead and shrink it remove the `--check`

```bash
quads --shrink --cloud cloud02 --weeks 2
```

### Shrinking the Schedule of a Specific Host

You might also want to shrink the lifetime of a specific host.
In this example we'll be shrinking the assignment end date for host01.

```bash
quads --shrink --host host01 --weeks 2 --check
```

This will check whether or not the host schedule can be shrunk without conflicts.

To go ahead and shrink it remove the `--check`

```bash
quads --shrink --host host01 --weeks 2
```

### Terminating a Schedule

If you would like to terminate the lifetime of a schedule at either a host or cloud level, you can pass the `--now` argument instead of `--weeks` which will set the schedules end date to now.
In this example we'll be terminating the assignment end date for cloud02.

```bash
quads --shrink --cloud cloud02 --now --check
```

This will check whether or not the environment can be terminated without conflicts.

To go ahead and terminate it remove the `--check`

```bash
quads --shrink --cloud cloud02 --now
```

### Adding Hosts to an existing Cloud

QUADS also supports adding new machines into an existing workload (cloud).

   - Search Availability Pool for Free Servers
      - Let's look for any 5 x servers from `2019-03-11 22:00` until `2019-04-22 22:00`

```bash
quads --ls-available --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00"

```
```
c03-h11-r620.rdu.openstack.example.com
c03-h13-r620.rdu.openstack.example.com
c03-h14-r620.rdu.openstack.example.com
c03-h15-r620.rdu.openstack.example.com
```

  - Move New Hosts into Existing Cloud

Above we see all the free servers during our timeframe, let's move them into cloud10

```bash
quads --host c03-h11-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads --host c03-h13-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads --host c03-h14-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
quads --host c03-h15-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
```

### Removing a Schedule

You can remove an existing schedule across a set of hosts using the ```--rm-schedule``` flag against the schedule ID for each particular machine of that assignment.

   - Example: removing the schedule for three machines in cloud
   - Obtain the schedule ID via ```quads --ls-schedule --host```
```bash
quads --rm-schedule --schedule-id 2
quads --rm-schedule --schedule-id 3
quads --rm-schedule --schedule-id 4
```

 * NOTE: Previous versions of QUADS required passing `--host`. This is not required on QUADS 2.0 onwards as the schedule Ids are now unique.

### Removing a Schedule across a large set of hosts

You should search for either the start or end dates to select the right schedule ID to remove when performing schedule removals across a large set of hosts.

   - If you are using QUADS in any serious capacity **always pick this option**.
   - Example: removing schedule by searching for start date.
   - Often machine schedule ID's are different for the same schedule across a set of machines, this ensures you remove the right one.

```bash
for host in $(cat /tmp/452851); do quads --rm-schedule --schedule-id $(quads --ls-schedule --host $host | grep cloud08 | grep "start=2017-08-06" | tail -1 | awk -F\| '{ print $1 }'); echo Done. ; done
```

### Removing a Host from QUADS

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```bash
quads --rm-host f03-h30-000-r720xd.rdu2.example.com
Removed: {'host': 'f03-h30-000-r720xd.rdu2.example.com'}
```

### Modifying a Host Schedule

* Host schedules are managed by unique schedule ID's which can be viewed via the `--ls-schedule` command.
* To modify a host schedule use the `--mod-schedule --schedule-id` command and either `--schedule-start` or `--schedule-end` or both as needed.
* Before using this, make sure it's not easier to simply use `--shrink` or `--extend` and sub-commands across the entire cloud/environments or even per-host first.

```bash
quads --mod-schedule --host host01.example.com --mod-schedule --schedule-id 31 --schedule-start "2023-05-22 22 :00" --schedule-end "2023-06-22 22:00"
```

#### Modifying a Host Schedule across a large set of hosts

* You may often need to modify the same schedule ID across a large set of hosts, in this scenario you can use the following one-liner:
* You will want to filter for the specific cloudname and at least one schedule start or stop identifier (since environments are re-used).
  * In this example we use `cloud06` and `start=2023-03-13` to make sure our `--mod-schedule` command is unique.
* It's also a good idea to do this first by prepending `echo` to `quads` to ensure that the `schedule-id` are matched.

```bash
for host in $(cat /tmp/2491); do quads --mod-schedule --schedule-id $(quads --ls-schedule --host $host | grep cloud06 | grep "start=2023-03-13" | tail -1 | awk -F\| '{ print $1 }') --host $host --schedule-start "2023-03-12 22:00" ; done
```


### Modify a Host Interface

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```bash
quads --mod-interface --interface-name em1 --host f03-h30-000-r720xd.rdu2.example.com --no-pxe-boot
Interface successfully updated
```

### Remove a Host Interface

To remove a host entirely from QUADS management you can use the `--rm-host` command.

```bash
quads --rm-interface --interface-name em1 --host f03-h30-000-r720xd.rdu2.example.com
Resource properly removed
```

## Using the QUADS JSON API
* All QUADS actions under the covers uses the [JSON API v3](/docs/quads-api.md)

## Filtering Systems by Hardware Capability
* We provide a flexible host hardware [metadata and filtering model](/docs/quads-host-metadata-search.md) via the API.

## Additional Tools and Commands

### Verify or Correct Cloud and Host Network Switch Settings
* The tool `/opt/quads/quads/verify_switchconf.py` can be used to both validate and correct network switch configs.
* This can be run at a cloud level (and with 1.1.5+ also at the per-host level).
* It's advised to run it first without `--change` to see if it would fix something.
* This will also check/correct optional routable VLANs if those are in use.
* To validate a clouds network config:

```bash
/opt/quads/quads/tools/verify_switchconf.py --cloud cloud10
```

* To validate and fix a clouds network config use `--change`

```bash
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
```bash
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

```bash
/opt/quads/quads/tools/modify_switch_conf.py --host host01.example.com --nic1 1400 --nic2 1401 --nic3 1400 --nic4 1402 --nic5 1400
```
* All `--nic*` arguments are optional so this can be also done individually for all nics.

#### Mapping Interface to VLAN ID
* An easy way to figure out what VLAN corresponds to what generic `em` interface in the QUADS `--ls-interfaces` information we now include the following tool:
```bash
./opt/quads/quads/tools/ls_switch_conf.py --cloud cloud32
INFO - Cloud qinq: 1
INFO - Interface em1 appears to be a member of VLAN 1410
INFO - Interface em2 appears to be a member of VLAN 1410
```

This tool also accepts the `--all` argument which will list a detail for all hosts in the cloud.

Additional you can achieve the same with the following shell one-liner, setting `cloud=XX` for the cloud and adjusting `$(seq 1 4)` for your interface ranges available on the host.

```bash
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

```bash
quads --mod-cloud --cloud cloud02 --cloud-owner jhoffa
```

```bash
quads --mod-cloud --cloud cloud04 --cc-users "tpetty, fmercury"
```

```bash
quads --mod-cloud --cloud cloud06 --vlan 604 --wipe
```

```bash
quads --mod-cloud --cloud cloud50 --no-wipe
```

```bash
quads --mod-cloud --cloud cloud50 --vlan none
```

### Looking into the Future
* Because QUADS knows about all future schedules you can display what your environment will look like at any point in time using the `--date` command.

* Looking into a specific environment by date

```bash
quads --cloud-only --cloud cloud08 --date "2019-06-04 22:00"
```

```
f16-h01-000-1029u.rdu2.example.com
f16-h02-000-1029u.rdu2.example.com
f16-h03-000-1029u.rdu2.example.com
f16-h05-000-1029u.rdu2.example.com
f16-h06-000-1029u.rdu2.example.com
```

* Looking at all schedules by date

```bash
quads --ls-schedule --date "2020-06-04 22:00"
```

### Dry Run for Pending Actions
* You can see what's in progress or set to provision via the ```--dry-run``` sub-flag of ```--move-hosts```

```bash
quads --move-hosts --dry-run
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

* You can use `quads --find-free-cloud` to suggest a cloud environment to use that does not have any future hosts scheduled to use it.

```bash
quads --find-free-cloud
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

```bash
quads --ls-available --schedule-start "2019-12-05 08:00" --schedule-end "2019-12-15 08:00"
```

  - Find based on starting now with an end range:

```bash
quads --ls-available --schedule-end "2019-06-02 22:00"
```

#### Find Available Hosts based on Hardware or Model

* In QUADS `1.1.4` and higher you can now filter your availability search based on hardware capabilities or model type.
* Using this feature requires [importing hardware metadata](/docs/quads-host-metadata-search.md#how-to-import-host-metadata)
* Example below using `--filter "model==1029U-TRTP"`

```bash
quads --ls-available --schedule-start "2020-08-02 22:00" --schedule-end "2020-08-16 22:00" --filter "model==1029U-TRTP"
```

* Listing retired hosts can now use the `--filter` feature:

```bash
quads --ls-hosts --filter "retired==True"
```

* Listing specific hosts from a certain cloud:

```bash
quads --cloud-only --cloud cloud13 --filter "model==FC640"
```

#### Find Available Web Interface

* We now have a Flask-based `--ls-available` web interface available on `quadshost`.
* This is provided via the `quads-web` systemd service.
* You will need to seed the `models` data for your systems using the new [host metadata feature](/docs/quads-host-metadata-search.md)

![quads-available-web](/image/quads-available-web.png)

* Control + click can select more than one model
* Not selecting a model assumes a search for anything available.

#### Find a System by MAC Address
* You can utilize the new metadata model and `--filter` command in `1.1.4` and above along with `--ls-hosts` to search for a system by MAC Address.

```bash
quads --ls-hosts --filter "interfaces.mac_address==ac:1f:6b:2d:19:48"
```

#### Find Systems by Switch IP Address
* You can list what systems are connected to a switch by querying the `ip_address` (soon to be `switch_ip` in 1.1.7) information from the interfaces datasource.

```bash
quads --ls-hosts --filter "interfaces.ip_address==10.1.34.210"
```

## Using JIRA with QUADS
* We utilize the JIRA ticketing system internally for R&D infrastructure requests managed by QUADS.
* We do provide some best-effort tooling and a JIRA library to bridge automation gaps.

   - For more information see [Using JIRA with QUADS](/docs/using-jira-with-quads.md)

## Backing up QUADS

* We do not implement backups for QUADS for you, but it's really easy to do on your own via Postgres [pg_dumpall](https://www.postgresql.org/docs/current/app-pg-dumpall.html)
```
su - postgres -c "pg_dumpall --clean > /tmp/quadsdb.sql"
```

* Configuration files are all kept in `/opt/quads/conf`


## Restoring QUADS from Backup
* You can restore a QUADS databasea via Postgres [psql](https://www.postgresqltutorial.com/postgresql-administration/postgresql-restore-database/) and everything is in the database and `/opt/quads/conf` files.
* Restoring just the quads database:

```
su - postgres -c "psql -d quads -f /tmp/quadsdb.sql"
```

* Restoring the entire database:

```
su - postgres -c "psql -f /tmp/quadsdb.sql"
```

## Troubleshooting Validation Failures
A useful part of QUADS is the functionality for automated systems/network validation.  Below you'll find some steps to help understand why systems/networks might not pass validation so you can address any issues.

### Understanding Validation Structure
There are two main validation tests that occur before a cloud environment is automatically released:

* **Foreman Systems Validation** ensures that no target systems in your environment are marked for build.
* **VLAN Network Validation** ensures that all the backend interfaces in your isolated VLANs are reachable via fping

All of these validations are run from `--validate-env` and we also ship a few useful tools to help you figure out validation failures.

`--validate-env` is run from cron, see our [example cron entry](cron/quads)

### Troubleshooting Steps
You should run through each of these steps manually to determine what systems/networks might need attention of automated validation does not pass in a reasonable timeframe.  Typically, `admin_cc:` will receieve email notifications of trouble hosts as well.


* **General Availability** can be checked via a simple `fping` command, this should be run first.

```bash
quads --cloud-only --cloud cloud23 > /tmp/cloud23
fping -u -f /tmp/cloud23
```

* **Foreman Systems Validation** can be run via the hammer cli command provided by `gem install hammer_cli_foreman_admin hammer_cli`

```bash
for host in $(quads --cloud-only --cloud cloud15) ; do echo $host $(hammer host info --name $host | grep -i build); done
```

No systems should be left marked for build.

### Validation using Debug Mode
* **NOTE** Automated validation **will not** start until 2 hours after the assignment is scheduled to go out, until this point `--validate-env` will not attempt to validate any systems if run and they have started less than 2 hours ago.
  - This can be set via the `validation_grace_period:` setting in `/opt/quads/conf/quads.yml`

* `--validate-env` now has a `--debug` option which tells you what's happening during validation.
* This will test the backend network connectivity part and the entire set of checks.

* **Successful Validation** looks like this:

```bash
quads --validate-env --debug
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

```bash
quads --validate-env --debug
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

```bash
quads --validate-env --skip-network
```

### Skipping Past Host and Systems Validation

* In `QUADS 1.1.8` you can skip past systems and host validation (Foreman) via:

```
/opt/quads/quads/tools/validate_env.py --skip-system
```

### Skipping Past Network and Systems Validation per Host

* In `QUADS 1.1.8` you can skip past both systems and network checks per host via:

```
/opt/quads/quads/tools/validate_env.py --skip-hosts host01.example.com host02.example.com
```

* Effectively, any host listed with `--skip-hosts` will pass it completely through validation.
* This can be used in combination with `--skip-system` and `--skip-network` as well.

### Validate Only a Specific Cloud

* If you want to validate only a certain cloud you can do so by specifying the cloud's name with the `--cloud` flag.
```bash
quads --validate-env --cloud cloud01
```

### Mapping Internal VLAN Interfaces to Problem Hosts
You might have noticed that we configure our [Foreman](https://github.com/redhat-performance/quads/tree/latest/templates/foreman) templates to drop `172.{16,17,18,19}.x` internal VLAN interfaces which correspond to the internal, QUADS-managed multi-tenant interfaces across a set of hosts in a cloud assignment.

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

This mapping feeds into our [VLAN network validation code](https://github.com/redhat-performance/quads/blob/latest/src/quads/tools/validate_env.py#L276)

### Validating after Removing Hosts
* There is currently a corner-case [bug](https://github.com/redhat-performance/quads/issues/361) where removing host(s) prior to the assignment being released may make `quads --validate-env` do nothing.
* You'll need to workaround this in the Postgres database:

  - Connect to postgres
```
sudo -u postgres psql
```
  - Connect to the QUADS database
```
postgres=# \c quads;
You are now connected to database "quads" as user "postgres".
```
  - Find the ID of your problem environment
```
quads=# select * from clouds where name = 'cloud17';
 id |  name   |   last_redefined
----+---------+---------------------
 18 | cloud17 | 2024-10-01 06:00:00
(1 row)
```
  - Look at the flags set for that environment, specifically `provisioned` if it's `f` or `t` (true or false)
```
quads=# select * from assignments where cloud_id = 18;
```

```
 id | active | provisioned | validated |   description    |  owner  | ticket | qinq | wipe |
                                                                         | cloud_id | vlan_id |        created_at
----+--------+-------------+-----------+------------------+---------+--------+------+------+-------------------------------------------------------
-------------------------------------------------------------------------+----------+---------+--------------------------
 54 | t      | f           | f         | template testing | wfoster | 3798   |    0 | t    | \x80059545000000000000008c1673716c616c6368656d792e6578
654c6973749493945d94288c0767726166756c73948c066b616d62697a9465859452942e |       18 |         | 2024-10-01 06:00:07.0437
(1 row)
```
  - Now toggle the `provisioned` flag to True (`t`)
```
quads=# update assignments set provisioned = true where id = 54;
UPDATE 1
```
  - Check one more time, it should have updated.
```
quads=# select * from assignments where cloud_id = 18;
 id | active | provisioned | validated |   description    |  owner  | ticket | qinq | wipe |
                                                                         | cloud_id | vlan_id |        created_at
----+--------+-------------+-----------+------------------+---------+--------+------+------+-------------------------------------------------------
-------------------------------------------------------------------------+----------+---------+--------------------------
 54 | t      | t           | f         | template testing | wfoster | 3798   |    0 | t    | \x80059545000000000000008c1673716c616c6368656d792e6578
654c6973749493945d94288c0767726166756c73948c066b616d62697a9465859452942e |       18 |         | 2024-10-01 06:00:07.0437
(1 row)
```
  - Now your new assignment should get proper attention from `quads --validate-env`

## Contact QUADS Developers

Besides Github we're also on IRC via `irc.libera.chat`.  You can [click here](https://web.libera.chat/?channels=#quads) to join in your browser.

## QUADS Talks and Media
[![Skynet your Infrastructure with QUADS @ EuroPython 2017](http://img.youtube.com/vi/9e1ZhtBliHc/0.jpg)](https://www.youtube.com/watch?v=9e1ZhtBliHc "Skynet your Infrastructure with QUADS")

   - [Skynet your Infrastructure with QUADS @ Europython 2017 Slides](https://hobosource.files.wordpress.com/2016/11/skynet_quads_europython_2017_wfoster.pdf)
   - [Skynet your Infrastructure with QUADS @ DevOps Pro Moscow 2018 Slides](https://hobosource.files.wordpress.com/2017/11/quads_devopspro_moscow_wfoster_2017-11-16.pdf)
