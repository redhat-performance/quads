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

quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
lockdir=$data_dir/lock
untouchable_hosts=${quads["untouchable_hosts"]}
ipmi_username=${quads["ipmi_username"]}
ipmi_password=${quads["ipmi_password"]}

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

declare -A cloud01=( ["em1"]="1100" ["em2"]="1101" ["em3"]="1102" ["em4"]="1103")
declare -A cloud02=( ["em1"]="1110" ["em2"]="1111" ["em3"]="1112" ["em4"]="1113")
declare -A cloud03=( ["em1"]="1120" ["em2"]="1121" ["em3"]="1122" ["em4"]="1123")
declare -A cloud04=( ["em1"]="1130" ["em2"]="1131" ["em3"]="1132" ["em4"]="1133")
declare -A cloud05=( ["em1"]="1140" ["em2"]="1141" ["em3"]="1142" ["em4"]="1143")
declare -A cloud06=( ["em1"]="1150" ["em2"]="1151" ["em3"]="1152" ["em4"]="1153")
declare -A cloud07=( ["em1"]="1160" ["em2"]="1161" ["em3"]="1162" ["em4"]="1163")
declare -A cloud08=( ["em1"]="1170" ["em2"]="1171" ["em3"]="1172" ["em4"]="1173")
declare -A cloud09=( ["em1"]="1180" ["em2"]="1181" ["em3"]="1182" ["em4"]="1183")
declare -A cloud10=( ["em1"]="1190" ["em2"]="1191" ["em3"]="1192" ["em4"]="1193")
declare -A cloud11=( ["em1"]="1200" ["em2"]="1201" ["em3"]="1202" ["em4"]="1203")
declare -A cloud12=( ["em1"]="1210" ["em2"]="1211" ["em3"]="1212" ["em4"]="1213")
declare -A cloud13=( ["em1"]="1220" ["em2"]="1221" ["em3"]="1222" ["em4"]="1223")
declare -A cloud14=( ["em1"]="1230" ["em2"]="1231" ["em3"]="1232" ["em4"]="1233")
declare -A cloud15=( ["em1"]="1240" ["em2"]="1241" ["em3"]="1242" ["em4"]="1243")
declare -A cloud16=( ["em1"]="1250" ["em2"]="1251" ["em3"]="1252" ["em4"]="1253")

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
    old_vlan=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show vlans interface ${switchport}.0 2>/dev/null| egrep ^VLAN | sed 's/VLAN Name: vlan\(.*\), Index.*/\1/g')
    if [ -z "$old_vlan" ]; then
        echo "Could not determine the previous VLAN for $host_to_move"
        exit 1
    fi

    case $new_cloud in
    cloud01)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud01["em1"]}
        else
            new_vlan=${cloud01[$interface]}
        fi
        ;;
    cloud02)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud02["em1"]}
        else
            new_vlan=${cloud02[$interface]}
        fi
        ;;
    cloud03)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud03["em1"]}
        else
            new_vlan=${cloud03[$interface]}
        fi
        ;;
    cloud04)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud04["em1"]}
        else
            new_vlan=${cloud04[$interface]}
        fi
        ;;
    cloud05)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud05["em1"]}
        else
            new_vlan=${cloud05[$interface]}
        fi
        ;;
    cloud06)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud06["em1"]}
        else
            new_vlan=${cloud06[$interface]}
        fi
        ;;
    cloud07)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud07["em1"]}
        else
            new_vlan=${cloud07[$interface]}
        fi
        ;;
    cloud08)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud08["em1"]}
        else
            new_vlan=${cloud08[$interface]}
        fi
        ;;
    cloud09)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud09["em1"]}
        else
            new_vlan=${cloud09[$interface]}
        fi
        ;;
    cloud10)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud10["em1"]}
        else
            new_vlan=${cloud10[$interface]}
        fi
        ;;
    cloud11)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud11["em1"]}
        else
            new_vlan=${cloud11[$interface]}
        fi
        ;;
    cloud12)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud12["em1"]}
        else
            new_vlan=${cloud12[$interface]}
        fi
        ;;
    cloud13)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud13["em1"]}
        else
            new_vlan=${cloud13[$interface]}
        fi
        ;;
    cloud14)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud14["em1"]}
        else
            new_vlan=${cloud14[$interface]}
        fi
        ;;
    cloud15)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud15["em1"]}
        else
            new_vlan=${cloud15[$interface]}
        fi
        ;;
    cloud16)
        if [ "$qinq" = "1" ]; then
            new_vlan=${cloud16["em1"]}
        else
            new_vlan=${cloud16[$interface]}
        fi
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
#### BEGIN FOREMAN REBUILD

if $rebuild ; then

  # first ensure PXE enabled on the host .... for foreman
  $bindir/pxe-foreman-config.sh $host_to_move

  # also determine whether or not to leverage post snipper for PXE disablement
  $bindir/pxe-director-config.sh $host_to_move

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
  hammer host update --name $host_to_move --build 1 --operatingsystem "RHEL 7"
  ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password chassis power off
  sleep 30
  ipmitool -I lanplus -H mgmt-$host_to_move -U $ipmi_username -P $ipmi_password chassis power on

fi

#### END FOREMAN REBUILD
# DONT update the wiki here.  This is costly and slows down the
# move of a large number of nodes.  Instead, run the wiki regeneration
# more frequently (via cron).  There's a lock file regardless so you
# cannot cause inconsistencies by running the cronjob more frequently.

# $bindir/regenerate-wiki.sh 1>/dev/null 2>&1

exit 0
