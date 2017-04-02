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

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
install_dir=${quads["install_dir"]}
quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
lockdir=$data_dir/lock
untouchable_hosts=${quads["untouchable_hosts"]}
ipmi_username=${quads["ipmi_username"]}
ipmi_password=${quads["ipmi_password"]}
ipmi_cloud_username_id=${quads["ipmi_cloud_username_id"]}

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

${current_dir}/move-and-rebuild-host-hil.py $host_to_move $old_cloud $new_cloud

exit 0
