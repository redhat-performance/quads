#!/bin/sh
#
# Dependencies: quads
#                  https://raw.githubusercontent.com/redhat-performance/quads/master/bin/quads.py
#               csv-to-instack.py
#                  https://raw.githubusercontent.com/redhat-performance/quads/master/bin/csv-to-instack.py
#
# This script is to work around an issue with RHEL OpenStack Director
# deployments REQUIRING PXE to be DISABLED on all interfaces except
# for the one used by director for OpenStack deployment.
# Not needed for general purpose environments.
#
# Called by: move-and-rebuild-host.sh
#####

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh
quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
foreman_director_parameter=${quads["foreman_director_parameter"]}

TARGET=$1
SCHEDULER=$quads

configdir=$data_dir/ports

CLOUD_LIST=$($SCHEDULER --ls-clouds)

# first host should be the undercloud

for cloud in $CLOUD_LIST ; do
    # if $data_dir/overcloud/$cloud exists it should contain a subset for hosts to
    # use in the instackenv.json
    # But it cannot contain arbitrary hostnames. Instead it can only contain
    # hosts that are already defined in the schedule for the $cloud env.

    if [ -f $data_dir/overcloud/$cloud ]; then
        TEMP_HOST_LIST=$(cat $data_dir/overcloud/$cloud | sort -u)
        FULL_HOST_LIST=$($SCHEDULER --cloud-only $cloud)
        HOST_LIST=""
        for h in $TEMP_HOST_LIST ; do
            for f in $FULL_HOST_LIST ; do
                if [ "$h" == "$f" ]; then
                    HOST_LIST="$HOST_LIST $h"
                fi
            done
        done
    else
        HOST_LIST=$($SCHEDULER --cloud-only $cloud)
    fi
    undercloud=""
    if [ -f $data_dir/undercloud/$cloud ]; then
        UC_HOST=$(cat $data_dir/undercloud/$cloud)
        FULL_HOST_LIST=$($SCHEDULER --cloud-only $cloud)
        for f in $FULL_HOST_LIST ; do
            if [ "$UC_HOST" == "$f" ]; then
                undercloud=$UC_HOST
            fi
        done
    fi
    for h in $HOST_LIST ; do
        if [ "$undercloud" == "" ]; then
          undercloud=$h
          if [ $h == "$TARGET" ]; then
            echo ==== set PXE to Foreman on $h
            # needs code here to set the foreman setting
            # for the %post action (e.g. director == false)
            hammer host set-parameter --host $h --name $foreman_director_parameter --value false
          fi
        fi
        if [ "$h" != "$undercloud" ]; then
          if [ $h == "$TARGET" ]; then
            echo ==== UNSET PXE from Foreman on $h
            # needs code here to set the foreman setting
            # for the %post action (e.g. director == false)
            hammer host set-parameter --host $h --name $foreman_director_parameter --value true
          fi
        fi
    done
done

