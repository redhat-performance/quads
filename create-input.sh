#!/bin/sh

# output might look like ....
cat > /dev/null <<EOF
   - This is [automatically generated](https://github.com/redhat-performance/ops-tools/tree/master/lab-scheduler).


**Rack C10**

| U-loc | Host | Serial | MAC | IP | OOB IP | OOB URL | OOB-MAC | Workload | Owner | Graph |
|-------|------|--------|-----|----|--------|---------|---------|----------|-------|-------|
| 1 |c10-h30-r630.openstack.example.com | JVKNZ1 | 00:01:AA:B4:A8 | 10.1.2.1 | 10.2.1.1 | [idrac](http://example.com) |01:AA:BC:7D:8A |cloud1 | wfoster | [grafana](http://example.com) |
EOF

# define your racks
racks="b08 b09 b10 c01 c02 c03 c08 c09 c10"

function print_header() {
    cat <<EOF

| U | ServerHostname | Serial | MAC | IP | IPMIADDR | IPMIURL | IPMIMAC | Workload | Owner | Graph |
|---|----------------|--------|-----|----|----------|---------|---------|----------|-------|-------|
EOF
}

function add_row() {
    # this assumes we are working with iDRAC (Dell specific) and we have ssh
    # keys setup. Also assumes working with hammer CLI (foreman). These bits can
    # be swapped out for alternate methods (or function extended to support
    # multiple platforms.

    arg=$1
    uloc=$2
    #echo $arg $uloc
    nodename=$(echo $arg | sed 's/mgmt-//')
    if [ ! -d /etc/lab/ipmi/$nodename ]; then
        mkdir -p /etc/lab/ipmi/$nodename
    fi
    if [ -f /etc/lab/ipmi/$nodename/svctag ]; then
        svctag=$(cat /etc/lab/ipmi/$nodename/svctag)
    else
        svctag=$(ssh -o PasswordAuthentication=false -o ConnectTimeout=10 $arg racadm getsysinfo 2>/dev/null | egrep "^Service Tag" | awk '{ print $NF }')
        echo $svctag > /etc/lab/ipmi/$nodename/svctag
    fi
    if [ -f /etc/lab/ipmi/$nodename/macaddr ]; then
        macaddr=$(cat /etc/lab/ipmi/$nodename/macaddr)
    else
        macaddr=$(ssh -o PasswordAuthentication=false -o ConnectTimeout=10 $arg racadm getsysinfo 2>/dev/null | egrep "^NIC.Integrated.1-1-1" | awk '{ print $NF }')
        echo $macaddr > /etc/lab/ipmi/$nodename/macaddr
    fi
    ip=$(host $nodename | awk '{ print $NF }')
    oobip=$(host $arg | awk '{ print $NF }')
    ooburl="[console](http://$arg/)"
    if [ -f /etc/lab/ipmi/$nodename/oobmacaddr ]; then
        oobmacaddr=$(cat /etc/lab/ipmi/$nodename/oobmacaddr)
    else
        oobmacaddr=$(hammer host info --name $arg | grep "MAC address" | awk '{ print $NF }')
        echo $oobmacaddr > /etc/lab/ipmi/$nodename/oobmacaddr
    fi
    workload=$(/root/schedule.py --host $nodename)
    # need to figure out owner
    owner=""
    # need to figure out grafana links
    grafana=""
    echo "| $uloc | $(echo $nodename | awk -F. '{ print $1 }') | $svctag | $macaddr | $ip | $oobip | $ooburl | $oobmacaddr | $workload | $owner | $grafana |"
}

# assume hostnames are the format "<rackname>-h<U location>-<type>"
function find_u() {
    echo $1 | awk -F- '{ print $3 }' | sed 's/^h//'
}

for rack in $racks ; do
    echo "**Rack "$(echo $rack | tr a-z A-Z)"**"
    print_header
    for h in $(hammer host list --per-page 10000 | grep mgmt | egrep -v 'cyclades|s4810|5548' | awk '{ print $3 }' | egrep $rack) ; do
        add_row $h $(find_u $h)
    done
    # add any special hosts that dont conform to naming ...
    if [ "$rack" == "c08" ]; then
        add_row mgmt-foreman.example.com 31
    fi
    echo ""

done
