QUADS (quick and dirty scheduler)
====================================

Automate scheduling and end-to-end provisioning of servers and networks.

* Please use our [Gerrit Review](https://review.gerrithub.io/#/q/project:redhat-performance/quads) to submit patches.
* We also have a [Trello board](https://trello.com/b/inFZ2nbD/quads) for tracking development.

![jenkins](/image/jenkins.png?raw=true)

![quads](/image/quads.jpg?raw=true)

   * [QUADS (quick and dirty scheduler)](#quads-quick-and-dirty-scheduler)
      * [What does it do?](#what-does-it-do)
      * [Notes](#notes)
      * [Requirements](#requirements)
      * [QUADS Workflow](#quads-workflow)
      * [Example: Systems Wiki](#example-systems-wiki)
      * [Example: Workload Assignments](#example-workload-assignments)
      * [Example: Calendar View](#example-calendar-view)
      * [Example: Systems Visualization Map](#example-systems-visualization-map)
      * [Example: IRC and Email Notifications](#example-irc-and-email-notifications)
      * [QUADS Usage Documentation](#quads-usage-documentation)
      * [Common Administration Tasks](#common-administration-tasks)
         * [Creating a New Cloud Assignment and Schedule](#creating-a-new-cloud-assignment-and-schedule)
         * [Extending the <strong>Schedule</strong> of an Existing
           Cloud](#extending-the-schedule-of-an-existing-cloud)
         * [Extending the <strong>Schedule</strong> of Existing Cloud with Differing
           Active Schedules](#extending-the-schedule-of-existing-cloud-with-differing-active-schedules)
         * [Extending Machine Allocation to an existing
           Cloud](#extending-machine-allocation-to-an-existing-cloud)
      * [Additional Tools and Commands](#additional-tools-and-commands)
      * [Contributing](#contributing)

## What does it do?
   - Create and manage a date/time based YAML schedule for machine allocations
   - Drive system provisioning and network switch changes based on workload assignment via external commands
   - Generates instackenv.json for each OpenStack environment.
   - Automatically generate documentation to illustrate current status, published to a [Wordpress instance](http://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html#pages)
     * Current system details
     * Current workloads and assignments
     * Current ownership and resource utilization links (grafana/collectd)
     * Total duration and time remaining in system assignments
   - Query scheduling data to determine future availability
   - Generates a monthly, auto-updated calendar of machine assignments
   - Generates a per-month visualization map for per-machine allocations to assignments.
   - RT (or similiar ticketing system) integration.
   - IRC bot and email notifications for new provisioning tasks and ones ending completion

## Notes
   - Very simple design (flat files, no external DB)
   - Allows for calling external provisioning commands via ```--path-to-command```
   - We use [Foreman](https://theforeman.org/) for the systems provisioning backend, but this can be substituted.

## Requirements
   - Python 2.6+ and libyaml (or [pyaml](https://pypi.python.org/pypi/pyaml)) are required for basic operation.
   - The scheduling functionality can be used standalone, but you'll want a provisioning backend like [Foreman](https://theforeman.org/) to take full advantage of QUADS scheduling, automation and provisioning capabilities.
   - To utilize the automatic wiki/docs generation we use [Wordpress](https://hobo.house/2016/08/30/auto-generating-server-infrastructure-documentation-with-python-wordpress-foreman/) but anything that accepts markdown via an API should work.
   - Switch/VLAN automation is done on Juniper Switches in [Q-in-Q VLANs](http://www.jnpr.net/techpubs/en_US/junos14.1/topics/concept/qinq-tunneling-qfx-series.html), but commandsets can easily be extended to support other network switch models.

## QUADS Workflow

![quadsworkflow](/image/quads-workflow.png?raw=true)


## Example: Systems Wiki

![wiki](/image/quads-wiki.png?raw=true)

## Example: Workload Assignments

![wiki](/image/quads-assignments.png?raw=true)

## Example: Calendar View

![wiki](/image/quads-calendar.png?raw=true)

## Example: Systems Visualization Map

![wiki](/image/quads-visual.png?raw=true)

## Example: IRC and Email Notifications
   - We notify our Supybot IRC bot to announce when new environments are provisioned

```
<lucius> QUADS: cloud02 : 9 (OSP Newton Testing) is now active, choo choo! - http://wiki.example.com/assignments/#cloud02
```
   - We send email notifications when new environments are defined.
   - We also send email notifications with the host list for the environment 7 days prior to activation.
   - Furthermore we send email notifications when new environments are provisioned.

```
Greetings Citizen,

You've been allocated a new environment!

cloud06 : 13 (OVN and OpenStack ML2/OVS)

(Details)
http://wiki.example.com/assignments/#cloud06

```
   - Lastly we send notifications 7, 5, 3, 1 days out from when assignments expire (or any number of machines are set to be removed during the current assignment schedule).
   - You can use the fields ```--cloud-owner``` and ```--cc-users``` to define who gets notifications.
```
This is a message to alert you that in 7 days
your allocated environment:

cloud08 : 29 (JBOSS Data Grid)

(Details)
http://wiki.example.com/assignments/#cloud08

will have some or all of the hosts expire.  Some or all of your
hosts will automatically be reprovisioned and returned to the
machine pool.

b01-h05-r620.example.com
b01-h06-r620.example.com
b02-h01-r620.example.com

```

## QUADS Usage Documentation
   - Initialize the schedule structure

```
mkdir /etc/lab
bin/quads.py --init
```

   - Define the various cloud environments

```
bin/quads.py --define-cloud cloud01 --description "Primary Cloud Environment"
bin/quads.py --define-cloud cloud02 --description "02 Cloud Environment"
bin/quads.py --define-cloud cloud03 --description "03 Cloud Environment"
```

   - Define the hosts in the environment

```
for h in $(hammer host list --per-page 1000 | grep -v mgmt | grep r630 | grep -v c08-h30 | awk '{ print $3 }') ; do bin/quads.py --define-host $h --default-cloud cloud01; done
```

   - To list the hosts:

```
bin/quads.py --ls-hosts
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
bin/quads.py --summary
```
```
cloud01 : 45 (Primary Cloud Environment)
cloud02 : 0 (02 Cloud Environment)
cloud03 : 0 (03 Cloud Environment)
```
   - Sync states of each host.
     - This needs to be done whenever a new host is created.
     - We also need to track the last configured environment of each host (this is how we track whether or not we need to reconfigure a host if the schedule changes).
     - *Note*: state files are stored in ```/opt/quads/state/HOSTNAME``` for each host and contains the current cloud membership

```
bin/quads.py --sync
```

   - Define a custom schedule for a host
     - Example: assign host ```c08-h21``` to the workload/cloud ```cloud02```

```
bin/quads.py --add-schedule --host c08-h21-r630.example.com --schedule-start "2016-07-11 08:00" --schedule-end "2016-07-12 08:00" --schedule-cloud cloud02
```

   - List the schedule for a specific host:

```
bin/quads.py --ls-schedule --host c08-h21-r630.example.com
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
bin/quads.py --move-hosts
```

You should see the following verbosity from a move operation

```
INFO: Moving c08-h21-r630.example.com from cloud01 to cloud02 c08-h21-r630.example.com cloud01 cloud02
```

In the above example the default move command was called ```/bin/echo``` for illustration purposes.  In order for this to do something more meaningful you should invoke the script with the ```--move-command``` option, which should be the path to a valid command.  The script takes three arguments (hostname, current cloud, new cloud).


   - Move a host using --move-command
     - You can append a script, command or other action as a post-hook (perhaps to fire off system provisioning).

```
bin/quads.py --move-hosts --path-to-command /usr/bin/movecommand.sh
```

## Common Administration Tasks

### Creating a New Cloud Assignment and Schedule

Creating a new schedule and assigning machines is currently done through the QUADS CLI.  There are a few options you'll want to utilize.

   - description (this will appear on the assignments dynamic wiki)
   -  force (needed for re-using an existing cloud)
   -  cloud-owner (for associating ownership and usage notifications)
   -  cc-users (Add additional people to notifications)
   -  cloud-ticket (RT ticket used for the work, also appears in the assignments dynamic wiki)
   -  VLAN design (optional, will default to 0 below)
     - ```qinq: 0``` (default) qinq VLAN separation by interface: primary, secondary and beyond QUADS-managed interfaces all match the same VLAN membership across other hosts in the same cloud allocation.  Each interface per host is in its own VLAN, and these match across the rest of your allocated hosts by interface (all nic1, all nic2, all nic3, all nic4 etc).
     - ```qinq: 1``` all QUADS-managed interfaces in the same qinq VLAN

```
bin/quads.py --define-cloud cloud03 --description "Messaging AMQ" --force --cloud-owner epresley --cc-users "jdoe jhoffa" --cloud-ticket 423625 --qinq 0
```

   - Now that you've defined your new cloud you'll want to allocate machines and a schedule.
     - We're going to find the first 20 Dell r620's and assign them as an example.

```
bin/quads.py --cloud-only cloud01 | grep r620 | head -20 > /tmp/RT423624
```

   - Now we'll allocate all of these hosts with a schedule, by default our system times use UTC.

```
for h in $(cat /tmp/RT423624) ; do bin/quads.py --host $h --add-schedule --schedule-start "2016-10-17 00:00" --schedule-end "2016-11-14 17:00" --schedule-cloud cloud03 ; done
```

That's it.  At this point your hosts will be queued for provision and move operations, we check once a minute if there are any pending provisioning tasks.  To check manually:

```
for h in $(./quads.py  --cloud-only cloud03) ; do echo -n ==== $h   :" " ; cat /etc/lab/state/$h ; done
```

After your hosts are provisioned and moved you should see them populate under the cloud list.

```
bin/quads.py --cloud-only cloud03
```

### Extending the __Schedule__ of an Existing Cloud

Occasionally you'll want to extend the lifetime of a particular assignment. QUADS lets you do this with one command but you'll want to double-check things first.
In this example we'll be extending the assignment end date for cloud03

   - First, get the updated list of current assignments

```
bin/quads.py --summary
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
bin/quads.py --ls-owner
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
bin/quads.py --cloud-only cloud03
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
bin/quads.py --host b09-h01-r620.rdu.openstack.example.com --ls-schedule
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
for h in $(bin/quads.py --cloud-only cloud03) ; do ./quads.py --host $h --mod-schedule 0 --schedule-end "2016-11-27 18:00"; done
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
for h in $(bin/quads.py --cloud-only cloud10) ; do echo bin/quads.py --mod-schedule $(bin/quads.py --ls-schedule --host $h | grep "urrent s" | awk -F: '{ print $2 }') --host $h --schedule-end "2017-01-09 05:00" ; echo Done. ; done
```

Note the difference in commands needed with the ```--mod-schedule``` flag that is required.

```
bin/quads.py --mod-schedule 0 --host b10-h11-r620.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
bin/quads.py --mod-schedule 3 --host c08-h21-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
bin/quads.py --mod-schedule 3 --host c08-h22-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
Done.
bin/quads.py --mod-schedule 2 --host c08-h23-r630.rdu.openstack.example.com --schedule-end 2017-01-09 05:00
```

  - **Approach: 2** Reschedule aginst a certain existing cloud:

```
for h in $(cat /tmp/CLOUD05TMP); do echo bin/quads.py --mod-schedule $(bin/quads.py --ls-schedule --host $h | grep cloud05 | tail -1 | awk -F\| '{ print $1 }') --host $h --schedule-start "2017-02-09 05:00" --schedule-end "2017-03-27 05:00" ; echo Done. ; done
```

  - **Approach: 3** Reschedule against a certain cloud **and** start date **(RECOMMENDED)**

```
for h in $(bin/quads.py --cloud-only cloud05); do echo bin/quads.py --mod-schedule $(bin/quads.py --ls-schedule --host $h | grep cloud05 | grep "start=2017-02-09" | tail -1 | awk -F\| '{ print $1 }') --host $h --schedule-start "2017-02-09 05:00" --schedule-end "2017-03-06 05:00" ; echo Done. ; done
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
bin/quads.py --host c03-h11-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
bin/quads.py --host c03-h13-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
bin/quads.py --host c03-h14-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
bin/quads.py --host c03-h15-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
bin/quads.py --host c03-h17-r620.rdu.openstack.example.com --add-schedule --schedule-start "2016-12-05 08:00" --schedule-end "2016-12-15 08:00" --schedule-cloud cloud10
```

* Note: You can run ```bin/find-available-py``` with the ```--cli``` flag to generate QUADS commands for you.

## Additional Tools and Commands

* You can display the allocation schedule on any given date via the ```--date``` flag.

```
bin/quads.py --date "2017-03-06"
```
```
cloud01:
  - b09-h01-r620.rdu.openstack.engineering.example.com
  - b09-h02-r620.rdu.openstack.engineering.example.com
  - b09-h03-r620.rdu.openstack.engineering.example.com
  - b09-h05-r620.rdu.openstack.engineering.example.com
  - b09-h06-r620.rdu.openstack.engineering.example.com
```

* You can use find-available.py to search for free machines for a timerange for allocation.
  - Use the optional ```-l``` option to filter results

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

* You can see what's in progress or set to provision via the ```--dry-run``` sub-flag of ```--move-hosts```

```
bin/quads.py --move-hosts --dry-run
```
```
INFO: Moving b10-h27-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h18-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h19-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h21-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h25-r620.rdu.openstack.example.com from cloud01 to cloud03
INFO: Moving c02-h26-r620.rdu.openstack.example.com from cloud01 to cloud03
```

* You can query all upcoming changes pending and what hosts are involved via the ```bin/quads-change-list.sh``` tool.

```
bin/quads-change-list.sh
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
bin/quads.py --ls-cc-users --cloud-only cloud04
```
```
epresley
```
   - To add or remove recipients they need to be added or removed with space separation and you'll need to redefine the cloud definition.
   - Get a list of all the atributes and redefine

```
bin/quads.py --full-summary | grep cloud04 ; bin/quads.py --ls-owner | grep cloud04 ; bin/quads.py --ls-ticket | grep cloud04 ; bin/quads.py --ls-cc-users --cloud-only cloud04
```
```
cloud04 : 52 (Ceph deployment)
cloud04 : jhoffa
cloud04 : 423424
epresley
```
   - Redefine

```
bin/quads.py --define-cloud cloud04 --description "Ceph Deployment" --force --cloud-owner jhoffa --cc-users "epresley rnixon" --cloud-ticket 423424
```
   - Now you can see the updated cc notifications

```
bin/quads.py --ls-cc-users --cloud-only cloud04
```
```
epresley
rnixon
```

* We have Jenkins CI run against all Gerrit patchsets via the [QUADS Simulator 5000](https://github.com/redhat-performance/quads/blob/master/example/test-quads.sh) CI test script.

## Contributing
We use [Gerrit](https://review.gerrithub.io/#/q/project:redhat-performance/quads) for code review, to submit a patch perform the following:

* Clone our repository:

```
git clone https://github.com/redhat-performance/quads
```

* Setup username/email for git and gerrithub:

```
git config --global user.email "example@example.com"
git config --global user.name "example"
git config --global --add gitreview.username "example"
```

* Make your changes

```
cd quads
vi bin/quads.py
```
* Add a local commit with a meaningful, short title followed by a space and a summary (you can check our commit history for examples).

```
git add bin/quads.py
git commit
```

* Install git-review and run it for first time.

```
yum install git-review
git review -s
```

* Now submit your patchset with git review (future patches you only need to run ```git review```

```
git review
```

* If you want to make changes to your patchset you can run the ```git commit --amend``` command.

```
vi bin/quads.py
git commit --amend
git review
```

For each patchset our CI will run QUADS through all of the possible command variations, manipulate data and simulate running against systems and then vote on your change.  We will be constantly expanding CI checks in the future to possibly include testing against bare-metal hardware and switches as we improve QUADS.
