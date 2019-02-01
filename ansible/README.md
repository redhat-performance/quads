# Ansible Boot Order Playbooks for Dell Systems

This directory contains a set of Ansible boot order playbooks for Dell systems to arrange their boot interface order to either a `foreman` or `director` (OpenStack / PXE off internal interfaces) ordering scheme using the Dell racadm tool.

This allows users to set a Foreman host parameter that manages/enforces the physical BIOS interface boot order of their Dell hosts without having to do things manually.

This will be superceded by [badfish](https://github.com/redhat-performance/badfish) which is a redfish-based Python tool, for now we manage this with Ansible, Foreman host parameters and racadm within QUADS.

This functionality is optional, but we find it useful as we do a lot of OpenStack and internal (private VLAN) PXE-driven application workloads and generally try to do as much systems/network prep for transient tenants as possible ahead of time so they can concentrate on their actual performance and scale testing.

To utilize the functionality here take a look at the [Dell interface order config](https://github.com/redhat-performance/quads/blob/master/ansible/idrac_interfaces.yml) we reference that maps BIOS boot interface order to our constructs.

## How it Works
   * Foreman-managed systems within QUADS need the following host parameter set: `nullos: true` or `nullos: false`, this can be defined in [your QUADS conf.yaml](https://github.com/redhat-performance/quads/blob/master/conf/quads.yml#L183) via the `foreman_director_parameter:` variable.  Our default is `nullos:` which we'll be referring to in this document.

```
hammer host set-parameter --host host01.example.com --name nullos --value true
```
   * A persistent directory containing FQDN stub files is located in `/opt/quads/data/bootstate/` that contains a string, either `director` or `foreman` depending on the value of what you set as the Foreman host parameter above.

| Host Parameter | Value  | Boot Order  | Playbook that Runs |
|----------------|:-------| -----------:|-------------------:|
| nullos         | true   | director    |[Dell r620 Example](https://github.com/redhat-performance/quads/blob/master/ansible/racadm-setup-boot-r620-director.yml) |
| nullos         | false  | foreman     |[Dell r620 Example](https://github.com/redhat-performance/quads/blob/master/ansible/racadm-setup-boot-r620-foreman.yml) |

   * A [cronjob](https://github.com/redhat-performance/quads/blob/master/cron/quads#L11) runs the [quads-validate-boot-order](https://github.com/redhat-performance/quads/blob/master/bin/quads-validate-boot-order.sh) tool which creates both your `/opt/quads/data/boot` and `/opt/quads/data/bootstate` directory structure on the QUADS host, and then populates the value of each QUADS-managed host respective Foreman host parameter value at the time (translated to foreman or director above) into `/opt/quads/data/bootstate/$HOSTFQDN`.

   * Another [cronjob](https://github.com/redhat-performance/quads/blob/master/cron/quads#L10) runs the [quads-boot-order](https://github.com/redhat-performance/quads/blob/master/bin/quads-boot-order.sh) tool and runs the appropriate [ansible playbook](https://github.com/redhat-performance/quads/blob/master/ansible/idrac_interfaces.yml) depending on the Dell system type (we expect the model name somewhere in the hostname).  If you have a different boot order, combination or variation this is the file you want to edit.

      * An ansible inventory file is generated for each host so playbook interface ordering is run in parallel across your fleet.
      * A healthy QUADS environment will have **no files** under `/opt/quads/data/boot` and only each hosts current boot state reflected in `/opt/quads/data/bootstate/` for each host, this means that there are no pending interface order change actions.

| ../boot/$FQDN contains | ../bootstate/$FQDN contains | Action Taken |
|------------------------|-----------------------------|--------------|
| file empty | foreman | None |
| foreman | foreman | None |
| foreman | director | Run director playbook until successful |
| director | director | None |
| director | foreman  | Run foreman playbook until successful |


### Boot Order Mechanics

Interface boot order for each Dell host is managed via its Foreman host parameter in one central place and this is authoritative.

Of note, in the [quads-validate-boot-order](https://github.com/redhat-performance/quads/blob/master/bin/quads-validate-boot-order.sh) tool there is the concept of `build_state` and `current_state`.

`build_state` refers to whether a system has been marked for build by the user (upon reboot Foreman would kickstart provision the host).  `current_state` is the current value of the Foreman host parameter value set for `foreman_director_parameter:` (in our case this is nullos) for either true or false.

The following logic applies to the relationship between `current_state` and `build_state` in the [quads-validate-boot-        order](https://github.com/redhat-performance/quads/blob/master/bin/quads-validate-boot-order.sh) tool:

| Host Parameter | Value | Boot Order | Host Marked for Build? | Action |
|----------------|-------|------------|------|--------|
| nullos         | true  | director   | yes  | do not change boot order if build flag present |
| nullos         | false | foreman    | no   | nothing, assume this is intentional |

In other words, if your Dell system is marked for build in Foreman even if you have `nullos: true` it will not create an Ansible worker file in `/opt/quads/data/boot/$FQDN` until the system has succesfully been built or the build flag is toggled off.

### Provisioning Mechanics

In our examples we define the [move-and-rebuild-host.sh](https://github.com/redhat-performance/quads/blob/master/bin/move-and-rebuild-host.sh) as our `/opt/quads/bin/quads-cli --move-hosts --path-to-command` which calls our systems and network provisioning workflow.  Currently we flop interface ordering around to accomodate initial systems provisioning and then ultimately a default interface boot order, aiming primarily to accomodate OpenStack because it's the most demanding in terms of PXE order when using Triple-O/Ironic.

   * Systems set to be provisioned have their interface ordering stub created in `/opt/quads/data/boot/$FQDN` as `foreman`
   * Ansible playbooks fire off per [quads-boot-order](https://github.com/redhat-performance/quads/blob/master/bin/quads-boot-order.sh)
   * Once the Foreman `build: 0` state is achieved (system has been provisioned with an OS sucessfully), systems have their interface ordering stub created in `/opt/quads/data/boot/$FQDN` as `director`.
   * Ansible playbooks fire off again to swap interface order back to `director` ordering, [respective to their system type](https://github.com/redhat-performance/quads/blob/master/ansible/idrac_interfaces.yml).
   * Once the value of both `/opt/quads/data/boot/$FQDN` and `/opt/quads/data/bootstate/$FQDN` match this part is completed.
   * `/opt/quads/data/boot/$FQDN` should be empty for each host completing their provisioning lifecycle.

#### instackenv.json and OpenStack

By default the first host out of a cloud assignment has `nullos: false` set in its Foreman host parameter, which corresponds with `/opt/quads/data/bootstate/$FQDN` maintained as `foreman'.  This is because we typically associate this node in OpenStack deployments with an Undercloud node and users may need to reprovision occassionally without the complexity of swapping boot ordering or setting a one-time boot method via the iDRAC interface or badfish.

As an additional courtesy to OpenStack users, we also auto-generate and keep up to date an instackenv.json (OpenStack Triple-O installer answer file) via a [cronjob](https://github.com/redhat-performance/quads/blob/master/cron/quads#L12) and associated [make-instackenv-json](https://github.com/redhat-performance/quads/blob/master/bin/make-instackenv-json.sh) tool.

   * The first machine in a cloud assignment has `nullos: false` which omits it from the instackenv.json
   * Setting any hosts Foreman host parameter to `nullos: false` will omit that machine from the instackenv.json
   * If you want to do PXE services on one of your internal, QUADS-managed interfaces you will want to maintain `nullos: true` on all your machines as the director-style interface boot ordering permits this behavior.

### Known Issues

Sometimes racadm via Ansible simply cannot set the boot interface order correctly and will just keep running trying over and over.  If after several hours you still have $FQDN stub files in `/opt/quads/data/boot/` and `ansible-playbook` processes running chances are it will never complete (trust us, we've just let them go .. for science!).

The reasons behind this are varied:

   * Dell / racadm sometimes caches the output of `racadm get BIOS.BiosBootSettings.BootSeq`, so it feeds Ansible incorrect data to operate on perpetually.  **This is a vendor bug** and we've filed a few cases with Dell about this to no end.
   * Sometimes JobQueue gets hung, though Ansible tries to force clear it, sometimes only a FLEA power drain (unplug both PDU, hold power buttons for 60-120sec to drain all residual power, power back on or use our [PDU power on/off tools](https://github.com/redhat-performance/quads/blob/master/docs/pdu-setup.md) to address).
   * Other vendor problems, hardware issues, ghosts?

#### Workarounds

If you find yourself in a state where playbooks have had ample time to run and they just aren't doing the job, you can simply fake the interface order state and fix it manually.

   * Disable the cron jobs that check/manage boot interface order or utilize their settings:

```
###* * * * * /opt/quads/bin/quads-boot-order.sh 1>/dev/null 2>&1
###* * * * * /opt/quads/bin/quads-validate-boot-order.sh 1>/dev/null 2>&1
###* * * * * /opt/quads/bin/make-instackenv-json.sh 1>/dev/null 2>&1
```

   * Make a list of potential problem host(s)

```
ls /etc/lab/boot/*.com > /tmp/FIX-HOSTS.txt
```

   * Next, find which cloud(s) and proper settings your hosts should be set to:

```
cd /opt/quads/data/boot

for host in $(ls); do echo "====================="; printf "$host = "; cat $host; echo "state for $host = $(cat /etc/lab/bootstate/$host)"; echo "cloud is currently $(/opt/quads/bin/quads-cli  --ls-schedule --host $host | grep Default | awk '{print $3}')"; echo "foreman says $(hammer host info --name $host | grep -i nullos)"; done
```

   * Then simply match what the setting should be (e.g. director instead of foreman)

```
cd /opt/quads/boot/

for host in $(ls); do echo "director" > /opt/quads/data/bootstate/$host; done
```

   * Remove the `/opt/quads/data/boot/` stubs

```
cd /opt/quads/data/boot/

rm -f *.com
```

   * Investigate, fix, check your hosts.

```
cat /tmp/FIX-HOSTS.txt | sed -s 's/^/https\:\/\/mgmt-/g'
```

   * Enable cronjobs once all is well.

## Future Improvements

We're trying to automate around very old, inflexible legacy tools and BIOS/queueing systems riddled with decade-old bugs and oddities using Ansible, K.I.S.S. record/state keeping and enough user self-service to save ourselves a lot of time and effort.  Newer systems like iDRAC9 tend to have less of an issue here and none of this is a problem for SuperMicro as they only adopt a bare-bones IPMI version 2.0 spec which doesn't even allow you to juggle selective network interfaces in between localdisk for your boot order.

Like all things it can be improved, here's where we'll be going soon::

   * Move entirely to [badfish](https://github.com/redhat-performance/badfish) and the Redfish API
   * No longer juggle interface order to provision, instead utilize a one-shot boot approach (only PXE to provision on the Foreman interface when it needs to happen
   * Enforce only the `director` interface order, and only when machines are reclaimed but before they go out for another assignment.
