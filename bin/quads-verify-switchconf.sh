#!/bin/sh
#
# verify the switch configuration
# This is done per cloudenv, hance 1 argument is expected
#
# qinq states:
#     0 (nics separated)  (default)
#     1 (nics merged)     (all nics in same qinq)
##################################################

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
lockdir=$data_dir/lock
expect_script=$bindir/juniper-set-port.exp

args=`getopt -o c -l change -- "$@"`

function usage() {
    echo "Usage: `basename $0` [ -c,--change ] envname"
    echo "  e.g. `basename $0`    cloud11  (validate switch settings)"
    echo "       `basename $0` -c cloud11  (validate switch settings and change switch configs)"
}

if [ $? != 0 ] ; then usage ; echo "Terminating..." >&2 ; exit 1 ; fi

change=false

eval set -- "$args"
while true ; do
        case "$1" in
                -c|--change)
                        change=true ; shift ;
                        ;;
                --)
                        shift ; break ;
                        ;;
        esac
done

PIDFILE=$lockdir/quads-move.pid

if $change ; then
    echo === INFO: change requested
    if [ -f $PIDFILE ]; then
        while [ -d /proc/$(cat $PIDFILE) ]; do
            echo waiting on move to finish...
            sleep 1
        done
    fi
fi

echo $$ > $PIDFILE

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

if [ $# -ne 1 ]; then
    echo unexpected argument count.
    exit 1
fi

env=$1

if [ $($quads --cloud-only $env | wc -l) -eq 0 ]; then
    echo no hosts in $env
    exit 0
fi

qinq=$($quads --cloud-only $env --ls-qinq)

if [ -z "$qinq" ]; then
    qinq=0
fi

echo check configuration of $env for qinq state $qinq
echo ================================================
for h in $($quads --cloud-only $env) ; do
    echo === $h
    for interface in $(cat $data_dir/ports/$h) ; do
        ifname=$(echo $interface | awk -F, '{ print $1 }')
        switchip=$(echo $interface | awk -F, '{ print $3 }')
        switchport=$(echo $interface | awk -F, '{ print $5 }')
        case $env in
            cloud01)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud01["em1"]}
                else
                    vlan=${cloud01[$ifname]}
                fi
                ;;
            cloud02)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud02["em1"]}
                else
                    vlan=${cloud02[$ifname]}
                fi
                ;;
            cloud03)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud03["em1"]}
                else
                    vlan=${cloud03[$ifname]}
                fi
                ;;
            cloud04)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud04["em1"]}
                else
                    vlan=${cloud04[$ifname]}
                fi
                ;;
            cloud05)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud05["em1"]}
                else
                    vlan=${cloud05[$ifname]}
                fi
                ;;
            cloud06)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud06["em1"]}
                else
                    vlan=${cloud06[$ifname]}
                fi
                ;;
            cloud07)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud07["em1"]}
                else
                    vlan=${cloud07[$ifname]}
                fi
                ;;
            cloud08)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud08["em1"]}
                else
                    vlan=${cloud08[$ifname]}
                fi
                ;;
            cloud09)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud09["em1"]}
                else
                    vlan=${cloud09[$ifname]}
                fi
                ;;
            cloud10)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud10["em1"]}
                else
                    vlan=${cloud10[$ifname]}
                fi
                ;;
            cloud11)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud11["em1"]}
                else
                    vlan=${cloud11[$ifname]}
                fi
                ;;
            cloud12)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud12["em1"]}
                else
                    vlan=${cloud12[$ifname]}
                fi
                ;;
            cloud13)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud13["em1"]}
                else
                    vlan=${cloud13[$ifname]}
                fi
                ;;
            cloud14)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud14["em1"]}
                else
                    vlan=${cloud14[$ifname]}
                fi
                ;;
            cloud15)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud15["em1"]}
                else
                    vlan=${cloud15[$ifname]}
                fi
                ;;
            cloud16)
                if [ "$qinq" = "1" ]; then
                    vlan=${cloud16["em1"]}
                else
                    vlan=${cloud16[$ifname]}
                fi
                ;;
        esac
        qinqsetting=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show configuration interfaces ${switchport} 2>/dev/null | sed 's/^apply-groups QinQ_vl\(.*\);/\1/g')
        vlanmember=$(ssh -o passwordauthentication=no -o connecttimeout=3 $switchip show vlans interface ${switchport}.0 2>/dev/null| egrep ^VLAN | sed 's/VLAN Name: vlan\(.*\), Index.*/\1/g')
        sleep 2
        if [ "$qinqsetting" != "$vlan" ]; then
            echo "WARNING: interface ${switchport} not using QinQ_vl${vlan}"
        fi
        if [ "$vlanmember" != "$vlan" ] ; then
            echo "WARNING: interface ${switchport} appears to be a member of VLAN $vlanmember, should be $vlan"
        fi
        if $change ; then
            # call script to modify switch but only if all args present
            if [ "$vlanmember" != "$vlan" ] ; then
                if [ -z "$vlanmember" ]; then
                    echo "WARNING: currently unknown which VLAN is set"
                    echo "WARNING: setting to 1101"
                    vlanmember=1101
                fi
                echo CALLING: $expect_script $switchip $switchport $vlanmember $vlan
                $expect_script $switchip $switchport $vlanmember $vlan
            fi
        fi
    done
done
