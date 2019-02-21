#!/bin/sh
#
# Dependencies: quads
#                  https://raw.githubusercontent.com/redhat-performance/quads/master/bin/quads-cli
#               csv_to_instack.py
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
quads=${quads["install_dir"]}/bin/quads-cli
foreman_director_parameter=${quads["foreman_director_parameter"]}

TARGET=$1
CLOUD=$2
SCHEDULER=$quads

CLOUD_LIST=$($SCHEDULER --ls-clouds)

#
# This script is called only from the move-and-rebuild script.  The args
# passed are the host, and the cloud.  First host will be the undercloud
# Afterwards the user can change the default selected host for the undercloud
# by overriding the $foreman_director_parameter on a per host basis.
# For more information, see:
#   https://github.com/redhat-performance/quads/blob/master/templates/README.md
#

HOST_LIST=$($SCHEDULER --cloud-only $CLOUD)
for h in $HOST_LIST ; do
    if [ "$undercloud" == "" ]; then
      undercloud=$h
      if [ $h == "$TARGET" ]; then
        echo '==== set PXE to Foreman on '$h
        hammer host set-parameter --host $h --name $foreman_director_parameter --value false
      fi
    fi
    if [ "$h" != "$undercloud" ]; then
      if [ $h == "$TARGET" ]; then
        echo '==== UNSET PXE from Foreman on '$h
        hammer host set-parameter --host $h --name $foreman_director_parameter --value true
      fi
    fi
done

