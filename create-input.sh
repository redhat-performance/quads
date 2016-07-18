#!/bin/sh

# output might look like ....
cat > /dev/null <<EOF
   - This is [automatically generated](https://github.com/redhat-performance/ops-tools/tree/master/lab-scheduler).


**Rack C10**

| U-loc    |      Host                 | Serial | MAC  |  IP  |  OOB IP | OOB URL |  OOB-MAC     |  Workload  |  Owner  |  Graph                      |
|:---------|:--------------------------|:------|:-----|:------|:-------------|:-----------|:--------|:----------------------------|
|1         |c10-h30-r630.openstack.example.com  | JVKNZ1 | 00:01:AA:B4:A8|10.1.2.1|10.2.1.1|[idrac](http://example.com)|01:AA:BC:7D:8A|cloud1      |wfoster  |[grafana](http://example.com)|
|2         |                           |       |      |       |              |            |         |                             |
|3         |                           |       |      |       |              |            |         |                             |

**Rack C11**

| U-loc    |      Host     |  MAC  |  IP  |  OOB  |  OOB-MAC     |  Workload  |  Owner  |  Graph  |
|----------|:-------------:|------:|:----:|:-----:|:------------:|:----------:|:-------:|:-------:|
|          |               |       |      |       |              |            |         |         |
|          |               |       |      |       |              |            |         |         |
|          |               |       |      |       |              |            |         |         |

**Rack C12**

| U-loc    |      Host     |  MAC  |  IP  |  OOB  |  OOB-MAC     |  Workload  |  Owner  |  Graph  |
|----------|:-------------:|------:|:----:|:-----:|:------------:|:----------:|:-------:|:-------:|
|          |               |       |      |       |              |            |         |         |
|          |               |       |      |       |              |            |         |         |
|          |               |       |      |       |              |            |         |         |
EOF

# define your racks to generate for
racks="c08 c09 c10"

function print_header() {
    cat <<EOF

| U-loc    |      Host                 | Serial | MAC  |  IP  |  OOB IP | OOB URL |  OOB-MAC     |  Workload  |  Owner  |  Graph                      |
|:---------|:--------------------------|:------|:-----|:------|:-------------|:-----------|:--------|:----------------------------|
EOF
}
    
# note this currently is very Dell/iDRAC specific

function add_row() {
    arg=$1
    uloc=$2
    #echo $arg $uloc
    nodename=$(echo $arg | sed 's/mgmt-//')
    svctag=$(ssh $arg racadm getsysinfo 2>/dev/null | egrep "^Service Tag" | awk '{ print $NF }')
    macaddr=$(ssh $arg racadm getsysinfo 2>/dev/null | egrep "^NIC.Integrated.1-1-1" | awk '{ print $NF }')
    ip=$(host $nodename | awk '{ print $NF }')
    oobip=$(host $arg | awk '{ print $NF }')
    ooburl="[idrac](http://$arg/)"
    oobmacaddr=$(hammer host info --name $arg | grep "MAC address" | awk '{ print $NF }')
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
    for h in $(hammer host list --per-page 10000 | grep mgmt | egrep -v 'cyclades|s4810' | awk '{ print $3 }' | egrep $rack) ; do
        add_row $h $(find_u $h)
    done
    # add any special hosts that dont conform to naming ...
    if [ "$rack" == "c08" ]; then
        add_row mgmt-foreman.example.com 31
    fi
    echo ""

done
