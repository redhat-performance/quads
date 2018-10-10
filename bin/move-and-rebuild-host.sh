#!/bin/sh
#
# Takes three arguments
# e.g. : c08-h21-r630.example.com cloud01 cloud02
#
# Harcoding some assumptions:
# cloud01 uses:
#     em2 - vlan1101
#     em3 - vlan1102
#     em4 - vlan1103
# cloud02 uses:
#     em2 - vlan1111
#     em3 - vlan1112
#     em4 - vlan1113
# cloud03 uses:
#     em2 - vlan1121
#     em3 - vlan1122
#     em4 - vlan1123
#
# ... (currently up to cloud10)
#
####

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
lockdir=$data_dir/lock
untouchable_hosts=${quads["untouchable_hosts"]}
ipmi_username=${quads["ipmi_username"]}
ipmi_password=${quads["ipmi_password"]}
ipmi_cloud_username_id=${quads["ipmi_cloud_username_id"]}
spare_pool_name=${quads["spare_pool_name"]}

[ ! -d $lockdir ] && mkdir -p $lockdir

PIDFILE=$lockdir/quads-move.pid

if [ -f $PIDFILE ]; then
    if [ -d /proc/$(cat $PIDFILE) ]; then
        echo Another instance already running. Try again later.
        exit 1
    fi
fi

echo $$ > $PIDFILE

host_to_move=$1
old_cloud=$2
new_cloud=$3
rebuild=$4

if [ "$rebuild" = "" ]; then
    rebuild=true
else
    rebuild=false
fi

expect_script=$bindir/juniper-set-port.exp

declare -A offsets=( ["em1"]="0" ["em2"]="1" ["em3"]="2" ["em4"]="3")

configdir=$data_dir/ports

if [ ! -f $configdir/$host_to_move ]; then
    echo No data found in $configdir/$host_to_move
    exit 1
fi

for redalert in $untouchable_hosts ; do
    if [ "$host_to_move" == $redalert ]; then
        echo no way ....
        exit 1
    fi
done

qinq=$($quads --cloud-only $new_cloud --ls-qinq)

if [ -z "$qinq" ]; then
    qinq=0
fi

for line in $(cat $configdir/$host_to_move); do
    interface=$(echo $line | awk -F, '{ print $1 }')
    switchip=$(echo $line | awk -F, '{ print $3 }')
    switchtype=$(echo $line | awk -F, '{ print $4 }')
    switchport=$(echo $line | awk -F, '{ print $5 }')
    old_vlan=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show configuration interfaces ${switchport} 2>/dev/null | grep 'QinQ' | awk '{ print $2 }' | sed -e 's/QinQ_vl//' -e 's/;//')
    if [ -z "$old_vlan" ]; then
        echo "Warning: Could not determine the previous VLAN for $host_to_move on $interface, switch $switchip, switchport $switchport"
    else
        old_cloud_num=$(echo $old_cloud | sed 's/cloud//')
        old_cloud_offset=$(expr $old_cloud_num \* 10)
        old_base_vlan=$(expr 1090 + $old_cloud_offset)
        if [ "$qinq" = "1" ]; then
            old_vlan=$(expr $old_base_vlan + ${offsets["em1"]})
        else
            old_vlan=$(expr $old_base_vlan + ${offsets[$interface]})
        fi
    fi

    new_cloud_num=$(echo $new_cloud | sed 's/cloud//')
    cloud_offset=$(expr $new_cloud_num \* 10)
    base_vlan=$(expr 1090 + $cloud_offset)
    if [ "$qinq" = "1" ]; then
        new_vlan=$(expr $base_vlan + ${offsets["em1"]})
    else
        new_vlan=$(expr $base_vlan + ${offsets[$interface]})
    fi

    if [ "$switch_type" == "ftos" ]; then
        # this needs some work
        :
    else
        # This needs WORK to ensure success. ASSUMING it works.
        $expect_script $switchip $switchport $old_vlan $new_vlan
    fi
done

# update the instackenv.json files
$bindir/make-instackenv-json.sh

# create/modify foreman views here
# approach:
#
# (on run)
# 1)   strip the Foreman cloudXX user of all prior roles
# 2)   reset the foreman cloudXX user password to the --cloud-ticket of the cloud
# 3)   apply the matching roles to correspond to the views that belong to cloudXX
# (on interval)
# 4)   watch the user-to-role mappings on a schedule to ensure they match in case there was a change during the lifetime of the schedule (hosts added or removed).

#### BEGIN FOREMAN VIEWS
hammer user remove-role --login $old_cloud --role $host_to_move
hammer user add-role --login $new_cloud --role $host_to_move

foreman_user_password=$($quads --ls-ticket --cloud-only $new_cloud)
if [ -z "$foreman_user_password" ]; then
    foreman_user_password=$ipmi_password
fi

hammer user update --login $new_cloud --password $foreman_user_password

#### END FOREMAN VIEWS
#### BEGIN IPMI ACCOUNT RESET
# this resets the user IPMI account password to the foreman password.
# this is typically the ticket number.
ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password user set password $ipmi_cloud_username_id $foreman_user_password
# ensure the user_id is set to operator and not administrator
ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password user priv $ipmi_cloud_username_id 0x4
#### END IPMI ACCOUNT RESET
#### BEGIN FOREMAN REBUILD

if $rebuild ; then
  if [ $new_cloud != "cloud01" ]; then

    # first ensure PXE enabled on the host .... for foreman
    $bindir/pxe-foreman-config.sh $host_to_move

    # also determine whether or not to leverage post snipper for PXE disablement
    $bindir/pxe-director-config.sh $host_to_move $new_cloud

    # either puppet facts or Foreman sometimes collect additional interface info
    # this is needed sometimes as a workaround: clean all non-primary interfaces previously collected
    skip_id=$(hammer host info --name $host_to_move | egrep -B 3 "nterface .primary, provision" | grep Id: | awk '{ print $NF }')
    TMPIFFILE=$(mktemp /tmp/IFXXXXXXX)
    hammer host info --name $host_to_move > $TMPIFFILE

    # remove extraneous interfaces collected prior to previous host usage
    for interface in $(grep Id $TMPIFFILE  | grep ')' | grep -v $skip_id | awk '{ print $NF }') ; do
        hammer host interface delete --host $host_to_move --id $interface
    done
    rm -f $TMPIFFILE

    # perform host rebuild, in future the OS here should be a variable, fix me.
    # we will also force a specific partition table and media option, you should
    # adjust this to your environment
    hammer host update --name $host_to_move --build 1 --operatingsystem "RHEL 7" --partition-table "generic-rhel7" --medium "RHEL local"
    ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password chassis power off
    sleep 30
    ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password chassis power on
  fi
fi

#### END FOREMAN REBUILD
# DONT update the wiki here.  This is costly and slows down the
# move of a large number of nodes.  Instead, run the wiki regeneration
# more frequently (via cron).  There's a lock file regardless so you
# cannot cause inconsistencies by running the cronjob more frequently.

# $bindir/regenerate-wiki.sh 1>/dev/null 2>&1

exit 0
