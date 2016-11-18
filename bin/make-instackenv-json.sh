#!/bin/sh
#
# Dependencies: quads
#                  https://raw.githubusercontent.com/redhat-performance/quads/master/bin/quads.py
#               csv-to-instack.py
#                  https://raw.githubusercontent.com/redhat-performance/quads/master/bin/csv-to-instack.py
#

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh
quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
ipmi_username=${quads["ipmi_username"]}
ipmi_password=${quads["ipmi_password"]}
json_web_path=${quads["json_web_path"]}

SCHEDULER=$quads
JSON_MAKER=$bindir/csv-to-instack.py
TMPCSVFILE=$(mktemp /tmp/csvfileXXXXXX)

configdir=$data_dir/ports

CLOUD_LIST=$($SCHEDULER --ls-clouds)

# assume we have apache and /var/www/html/cloud will be used
[ ! -d $json_web_path ] && mkdir -p $json_web_path

rm -f json_web_path/*.json

# first host should be the undercloud

for cloud in $CLOUD_LIST ; do
    echo "macaddress,ipmi url,ipmi user, ipmi password, ipmi tool" > $TMPCSVFILE

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
        fi
        mac=$(egrep ^em2 $configdir/$h | awk -F, '{ print $2 }')
        ipmi_url=mgmt-$h
        ipmi_user=$ipmi_username
        ipmi_password=$ipmi_password
        ipmi_tool=pxe_ipmitool
        if [ "$h" != "$undercloud" ]; then
            echo $mac,$ipmi_url,$ipmi_user,$ipmi_password,$ipmi_tool >> $TMPCSVFILE
        fi
    done
    python $JSON_MAKER --csv=$TMPCSVFILE 2>/dev/null > $json_web_path/${cloud}_${undercloud}_instackenv.json 
    chmod 644 $json_web_path/${cloud}_${undercloud}_instackenv.json
done
rm -f $TMPCSVFILE

