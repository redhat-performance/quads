#!/bin/sh
#
# Dependencies: quads
#                  https://github.com/redhat-performance/ops-tools/blob/master/lab-scheduler/schedule.py
#               csv-to-instack.py
#                  https://github.com/someuser/csv-to-instack
#
SCHEDULER=/root/schedule.py
JSON_MAKER=/root/csv-to-instack.py
TMPCSVFILE=$(mktemp /tmp/csvfileXXXXXX)

configdir=/etc/lab/ports

CLOUD_LIST=$($SCHEDULER --ls-clouds)

rm -f /var/www/html/cloud/*.json

# first host should be the undercloud

for cloud in $CLOUD_LIST ; do
    echo "macaddress,ipmi url,ipmi user, ipmi password, ipmi tool" > $TMPCSVFILE

    # if /etc/lab/overcloud/$cloud exists it should contain subset for hosts to
    # use in the instackenv.json
    # But it cannot contain arbitrary hostnames. Instead it can only contain
    # hosts that are already defined in the schedule for the $cloud env.

    if [ -f /etc/lab/overcloud/$cloud ]; then
        TEMP_HOST_LIST=$(cat /etc/lab/overcloud/$cloud | sort -u)
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
    if [ -f /etc/lab/undercloud/$cloud ]; then
        UC_HOST=$(cat /etc/lab/undercloud/$cloud)
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
        ipmi_user=root
        ipmi_password=YOUR_DRAC_PASSWORD
        ipmi_tool=pxe_ipmitool
        if [ "$h" != "$undercloud" ]; then
            echo $mac,$ipmi_url,$ipmi_user,$ipmi_password,$ipmi_tool >> $TMPCSVFILE
        fi
    done
    python $JSON_MAKER --csv=$TMPCSVFILE 2>/dev/null > /var/www/html/cloud/${cloud}_${undercloud}_instackenv.json 
    chmod 644 /var/www/html/cloud/${cloud}_${undercloud}_instackenv.json
done
rm -f $TMPCSVFILE

