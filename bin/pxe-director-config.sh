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
CLOUD=$2
SCHEDULER=$quads

configdir=$data_dir/ports

CLOUD_LIST=$($SCHEDULER --ls-clouds)

# first host should be the undercloud

HOST_LIST=$($SCHEDULER --cloud-only $CLOUD)
for h in $HOST_LIST ; do
    if [ "$undercloud" == "" ]; then
      undercloud=$h
      if [ $h == "$TARGET" ]; then
        echo ==== set PXE to Foreman on $h
        hammer host set-parameter --host $h --name $foreman_director_parameter --value false
      fi
    fi
    if [ "$h" != "$undercloud" ]; then
      if [ $h == "$TARGET" ]; then
        echo ==== UNSET PXE from Foreman on $h
        hammer host set-parameter --host $h --name $foreman_director_parameter --value true
      fi
    fi
done

