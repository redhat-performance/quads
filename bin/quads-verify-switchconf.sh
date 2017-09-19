#!/bin/sh
#
# verify the switch configuration
# This is done per cloudenv, hance 1 argument is expected
#
# qinq states:
#     0 (nics separated)  (default)
#     1 (nics merged)     (all nics in same qinq)
##################################################

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
lockdir=$data_dir/lock
expect_script=$bindir/juniper-set-port.exp

args=`getopt -o c -l change -- "$@"`

function usage() {
    echo "Usage: `basename $0` [ -c,--change ] envname"
    echo "  e.g. `basename $0`    cloud11  (validate switch settings)"
    echo "       `basename $0` -c cloud11  (validate switch settings and change switch configs)"
}

if [ $? != 0 ] ; then usage ; echo "Terminating..." >&2 ; exit 1 ; fi

change=false

eval set -- "$args"
while true ; do
        case "$1" in
                -c|--change)
                        change=true ; shift ;
                        ;;
                --)
                        shift ; break ;
                        ;;
        esac
done

PIDFILE=$lockdir/quads-move.pid

if $change ; then
    echo '=== INFO: change requested'
    if [ -f $PIDFILE ]; then
        while [ -d /proc/$(cat $PIDFILE) ]; do
            echo waiting on move to finish...
            sleep 1
        done
    fi
fi

echo $$ > $PIDFILE

declare -A offsets=( ["em1"]="0" ["em2"]="1" ["em3"]="2" ["em4"]="3")

if [ $# -ne 1 ]; then
    echo unexpected argument count.
    exit 1
fi

env=$1

if [ $($quads --cloud-only $env | wc -l) -eq 0 ]; then
    echo no hosts in $env
    exit 0
fi

qinq=$($quads --cloud-only $env --ls-qinq)

if [ -z "$qinq" ]; then
    qinq=0
fi

echo check configuration of $env for qinq state $qinq
echo '================================================'
for h in $($quads --cloud-only $env) ; do
    echo '=== '$h
    for interface in $(cat $data_dir/ports/$h) ; do
        ifname=$(echo $interface | awk -F, '{ print $1 }')
        switchip=$(echo $interface | awk -F, '{ print $3 }')
        switchport=$(echo $interface | awk -F, '{ print $5 }')
        env_num=$(echo $env | sed 's/cloud//')
        env_offset=$(expr $env_num \* 10)
        base_vlan=$(expr 1090 + $env_offset)
        if [ "$qinq" = "1" ]; then
            vlan=$(expr $base_vlan + ${offsets["em1"]})
        else
            vlan=$(expr $base_vlan + ${offsets[$interface]})
        fi

        qinqsetting=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show configuration interfaces ${switchport} 2>/dev/null | sed 's/^apply-groups QinQ_vl\(.*\);/\1/g')
        vlanmember=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show vlans interface ${switchport}.0 2>/dev/null| egrep ^VLAN | sed 's/VLAN Name: vlan\(.*\), Index.*/\1/g')
        sleep 2
        if [ "$qinqsetting" != "$vlan" ]; then
            echo "WARNING: interface ${switchport} not using QinQ_vl${vlan}"
        fi
        if [ "$vlanmember" != "$vlan" ] ; then
            echo "WARNING: interface ${switchport} appears to be a member of VLAN $vlanmember, should be $vlan"
        fi
        if $change ; then
            # call script to modify switch but only if all args present
            if [ "$vlanmember" != "$vlan" ] ; then
            if [ -z "$vlanmember" -o "$(expr "$vlanmember" + 0 2>/dev/null)" != "$vlanmember" ]; then
                    echo "WARNING: currently unknown which VLAN is set"
                    echo "WARNING: setting to 1101"
                    vlanmember=1101
                fi
                echo CALLING: $expect_script $switchip $switchport $vlanmember $vlan
                $expect_script $switchip $switchport $vlanmember $vlan
            fi
        fi
    done
done
