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
ipmi_username=${quads["ipmi_cloud_username"]}
ipmi_password=${quads["ipmi_password"]}
json_web_path=${quads["json_web_path"]}
foreman_parameter=${quads["foreman_director_parameter"]}
domain=${quads["domain"]}

SCHEDULER=$quads
JSON_MAKER=$bindir/csv-to-instack.py
TMPCSVFILE=$(mktemp /tmp/csvfileXXXXXX)
TMPJSONFILE=$(mktemp /tmp/jsonXXXXXXX)

configdir=$data_dir/ports

CLOUD_LIST=$($SCHEDULER --ls-clouds)

# assume we have apache and /var/www/html/cloud will be used
[ ! -d $json_web_path ] && mkdir -p $json_web_path

rm -f json_web_path/*.json

# undercloud just means the hosts that are ignored from the instackenv.
# This is the list of hosts that have nullos=false.  The default is
# the first host in an environment when it is first created.

for cloud in $CLOUD_LIST ; do
    echo "macaddress,ipmi url,ipmi user, ipmi password, ipmi tool" > $TMPCSVFILE
    foreman_user_password=$($quads --ls-ticket --cloud-only $cloud)
    if [ -z "$foreman_user_password" ]; then
        foreman_user_password=$ipmi_password
    fi

    HOST_LIST=$($SCHEDULER --cloud-only $cloud)
    undercloud="$(hammer host list --search params.${foreman_param}=false | grep $domain  | awk '{ print $3 }' )"
    for h in $HOST_LIST ; do
        is_undercloud=false
        for uc in $undercloud ; do
            if [ "$h" = "$uc" ]; then
                is_undercloud=true
            fi
        done
        mac=$(egrep ^em2 $configdir/$h | awk -F, '{ print $2 }')
        ipmi_url=mgmt-$h
        ipmi_tool=pxe_ipmitool
        if ! $is_undercloud ; then
            echo $mac,$ipmi_url,$ipmi_username,$foreman_user_password,$ipmi_tool >> $TMPCSVFILE
        fi
    done
    python $JSON_MAKER --csv=$TMPCSVFILE 2>/dev/null > $TMPJSONFILE
    if cmp -s $TMPJSONFILE $json_web_path/${cloud}_instackenv.json ; then
        :
    else
        # possibly figure out if a notification can go out
        /bin/cp -p $json_web_path/${cloud}_instackenv.json $json_web_path/${cloud}_instackenv.json_$(date +"%Y-%m-%d_%H:%M:%S")
        /bin/cp $TMPJSONFILE $json_web_path/${cloud}_instackenv.json
    fi
    chmod 644 $json_web_path/${cloud}_instackenv.json
done
rm -f $TMPCSVFILE $TMPJSONFILE
