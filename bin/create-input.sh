#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
quads_url=${quads["quads_url"]}
rt_url=${quads["rt_url"]}
data_dir=${quads["data_dir"]}
exclude_hosts=${quads["exclude_hosts"]}
domain=${quads["domain"]}
# define your racks
racks=${quads["racks"]}

# output might look like ....
cat > /dev/null <<EOF
   - This is [automatically generated](https://github.com/redhat-performance/ops-tools/tree/master/lab-scheduler).


**Rack C10**

| U-loc | Host | Serial | MAC | IP | OOB IP | OOB URL | OOB-MAC | Workload | Owner | Graph |
|-------|------|--------|-----|----|--------|---------|---------|----------|-------|-------|
| 1 |c10-h30-r630.openstack.example.com | JVKNZ1 | 00:01:AA:B4:A8 | 10.1.2.1 | 10.2.1.1 | [idrac](http://example.com) |01:AA:BC:7D:8A |cloud1 | someuser | [grafana](http://example.com) |
EOF


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
    if [ ! -d $data_dir/ipmi/$nodename ]; then
        mkdir -p $data_dir/ipmi/$nodename
    fi
    svctag=$(cat $data_dir/ipmi/$nodename/svctag 2>/dev/null)
    if [ -f $data_dir/ipmi/$nodename/macaddr ]; then
        macaddr=$(cat $data_dir/ipmi/$nodename/macaddr)
    else
        macaddr=$(hammer host info --name $nodename | grep "MAC:" | awk '{ print $NF }')
        echo $macaddr > $data_dir/ipmi/$nodename/macaddr
    fi
    ip=$(host $nodename | awk '{ print $NF }')
    oobip=$(host $arg | awk '{ print $NF }')
    ooburl="<a href=http://$arg/ target=_blank>console</a>"
    if [ -f $data_dir/ipmi/$nodename/oobmacaddr ]; then
        oobmacaddr=$(cat $data_dir/ipmi/$nodename/oobmacaddr)
    else
        oobmacaddr=$(hammer host info --name $arg | grep "MAC:" | awk '{ print $NF }')
        echo $oobmacaddr > $data_dir/ipmi/$nodename/oobmacaddr
    fi
    workload=$($quads --host $nodename)
    # need to figure out owner
    if [ "$workload" == "None" ]; then
        owner=""
    else
        owner=$($quads --ls-owner --cloud-only $workload)
    fi
    # need to figure out grafana links
    grafana=""
    echo "| $uloc | $(echo $nodename | awk -F. '{ print $1 }') | $svctag | $macaddr | $ip | $oobip | $ooburl | $oobmacaddr | [$workload](/assignments/#$workload) | $owner | $grafana |"
}

# assume hostnames are the format "<rackname>-h<U location>-<type>"
function find_u() {
    echo $1 | awk -F- '{ print $3 }' | sed 's/^h//'
}

TMPHAMMERFILE1=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
TMPHAMMERFILE2=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --per-page 10000 1>$TMPHAMMERFILE1 2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
cat $TMPHAMMERFILE1 | grep mgmt | egrep -v "${exclude_hosts}" | awk '{ print $3 }' 1>$TMPHAMMERFILE2 2>&1

for rack in $racks ; do
    echo "**Rack "$(echo $rack | tr a-z A-Z)"**"
    print_header
    for h in $(cat $TMPHAMMERFILE2 | egrep $rack) ; do
        add_row $h $(find_u $h)
    done
    echo ""

done

rm -f $TMPHAMMERFILE1 $TMPHAMMERFILE2

