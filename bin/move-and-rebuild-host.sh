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

PIDFILE=/var/log/quads-move.pid

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

expect_script=/root/juniper-set-port.exp

declare -A cloud01=( ["em2"]="1101" ["em3"]="1102" ["em4"]="1103")
declare -A cloud02=( ["em2"]="1111" ["em3"]="1112" ["em4"]="1113")
declare -A cloud03=( ["em2"]="1121" ["em3"]="1122" ["em4"]="1123")
declare -A cloud04=( ["em2"]="1131" ["em3"]="1132" ["em4"]="1133")
declare -A cloud05=( ["em2"]="1141" ["em3"]="1142" ["em4"]="1143")
declare -A cloud06=( ["em2"]="1151" ["em3"]="1152" ["em4"]="1153")
declare -A cloud07=( ["em2"]="1161" ["em3"]="1162" ["em4"]="1163")
declare -A cloud08=( ["em2"]="1171" ["em3"]="1172" ["em4"]="1173")
declare -A cloud09=( ["em2"]="1181" ["em3"]="1182" ["em4"]="1183")
declare -A cloud10=( ["em2"]="1191" ["em3"]="1192" ["em4"]="1193")

configdir=/etc/lab/ports

if [ ! -f $configdir/$host_to_move ]; then
    echo No data found in $configdir/$host_to_move
    exit 1
fi

if [ "$host_to_move" == "foreman.example.com" ]; then
    echo no way ....
    exit 1
fi

if [ "$host_to_move" == "c08-h30-r630.example.com" ]; then
    echo no way ....
    exit 1
fi

for line in $(cat $configdir/$host_to_move); do
    interface=$(echo $line | awk -F, '{ print $1 }')
    switchip=$(echo $line | awk -F, '{ print $3 }')
    switchtype=$(echo $line | awk -F, '{ print $4 }')
    switchport=$(echo $line | awk -F, '{ print $5 }')
    case $old_cloud in
    cloud01)
        old_vlan=${cloud01[$interface]}
        ;;
    cloud02)
        old_vlan=${cloud02[$interface]}
        ;;
    cloud03)
        old_vlan=${cloud03[$interface]}
        ;;
    cloud04)
        old_vlan=${cloud04[$interface]}
        ;;
    cloud05)
        old_vlan=${cloud05[$interface]}
        ;;
    cloud06)
        old_vlan=${cloud06[$interface]}
        ;;
    cloud07)
        old_vlan=${cloud07[$interface]}
        ;;
    cloud08)
        old_vlan=${cloud08[$interface]}
        ;;
    cloud09)
        old_vlan=${cloud09[$interface]}
        ;;
    cloud10)
        old_vlan=${cloud10[$interface]}
        ;;
    *)
        echo unknown cloud $old_cloud
        exit 1
    esac


    case $new_cloud in
    cloud01)
        new_vlan=${cloud01[$interface]}
        ;;
    cloud02)
        new_vlan=${cloud02[$interface]}
        ;;
    cloud03)
        new_vlan=${cloud03[$interface]}
        ;;
    cloud04)
        new_vlan=${cloud04[$interface]}
        ;;
    cloud05)
        new_vlan=${cloud05[$interface]}
        ;;
    cloud06)
        new_vlan=${cloud06[$interface]}
        ;;
    cloud07)
        new_vlan=${cloud07[$interface]}
        ;;
    cloud08)
        new_vlan=${cloud08[$interface]}
        ;;
    cloud09)
        new_vlan=${cloud09[$interface]}
        ;;
    cloud10)
        new_vlan=${cloud10[$interface]}
        ;;
    *)
        echo unknown cloud $new_cloud
        exit 1
    esac

    if [ "$switch_type" == "ftos" ]; then
        # this needs some work
        :
    else
        # This needs WORK to ensure success. ASSUMING it works.
        $expect_script $switchip $switchport $old_vlan $new_vlan
    fi
done

# update the instackenv.json files
/root/make-instackenv-json.sh

if $rebuild ; then
  hammer host update --name $host_to_move --build 1 --operatingsystem "RHEL 7"
  ipmitool -I lanplus -H mgmt-$host_to_move -U root -P YOUR_DRAC_PASSWORD chassis power off
  sleep 90
  ipmitool -I lanplus -H mgmt-$host_to_move -U root -P YOUR_DRAC_PASSWORD chassis power on
fi

# update the wiki
/root/ops-tools/lab-scheduler/regenerate-wiki.sh 1>/dev/null 2>&1

exit 0

