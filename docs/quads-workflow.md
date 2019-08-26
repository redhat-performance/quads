# QUADS Architecture, Workflow and Visuals

Below are common workflows, visualizations and features of QUADS.

* [QUADS Workflow and Examples)](#quads-workflow-and-visuals)
    * [QUADS Architecture](#quads-architecture)
    * [QUADS Data Structure](#quads-data-structure)
    * [QUADS Workflow](#quads-workflow)
    * [QUADS Foreman Provisioning Workflow](#quads-foreman-provisioning-workflow)
    * [QUADS Move and Rebuild Provisioning UML](#quads-move-and-rebuild-provisioning-uml)
    * [Example: Automated Scheduling](#example-automated-scheduling)
    * [Example: Systems Wiki](#example-systems-wiki)
    * [Example: Workload Assignments](#example-workload-assignments)
    * [Example: Systems Visualization Map](#example-systems-visualization-map)
    * [Example: IRC and Email Notifications](#example-irc-and-email-notifications)

## QUADS Architecture
Typically this is how things look via our container orchestration.

![quadsarchitecture](../image/quads-container-architecture.png?raw=true)

## QUADS Data Structure
This is how our scheduling data, collections and data model within Mongo collections are stored.

![quads-erd-mongo](../image/quads-erd-mongo.png?raw=true)

## QUADS Workflow
More of a flat, "creative" process interpretation.

![quadsworkflow](../image/quads-workflow.png?raw=true)

## QUADS Foreman Provisioning Workflow
This is the workflow behind `quads/tools/move_and_rebuild_hosts.py`

![quadsforemanarch](../image/quads-foreman-workflow.png?raw=true)

## QUADS Move and Rebuild Provisioning UML
This is a UML chart illustrating all the API, host, switch and foreman workflows that happen when systems and networks are built and moved.

![quadsmoverebuild](../image/quads_provisioning_uml.png?raw=true)

## Example: Automated Scheduling

![quads-schedule](../image/quads-example-scheduling.png?raw=true)

## Example: Systems Wiki

![wiki](../image/quads-wiki.png?raw=true)

## Example: Workload Assignments

![wiki](../image/quads-assignments.png?raw=true)

## Example: Workload Assignments Readiness
We color-code progress bars and status based on total amount of completion for an entire assignment.

![wiki](../image/quads-assignment-readiness.png?raw=true)

## Example: Systems Visualization Map

![wiki](../image/quads-visual.png?raw=true)

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
