#!/bin/sh
# This parses the PDU to port mappings and generates
# the right port(s) required to perform power actions on
# a system.

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh
pdudir=${quads["install_dir"]}/bin

cd $pdudir

PDUFILE=$pdudir/PDU-connections.txt
host=$1
action=$2
shost=$(echo $host | awk -F. '{ print $1 }')
pdus=$(grep $shost $PDUFILE)

echo "Host: $host"
echo "Num of outlets: $(echo $pdus | wc -w)"
echo "=== Outlets:"
for outlet in $pdus ; do
    pdu=$(echo $outlet | awk -F, '{ print $1 }')
    socket=$(echo $outlet | awk -F, '{ print $2 }')
    if expr $socket + 0 1>/dev/null 2>&1 ; then
        driver=APC
    else
        driver=ServerTech
    fi
    echo "PDU: $pdu"
    echo "Socket: $socket"
    echo "Driver: $driver"
    if [ "$driver" = "APC" ]; then
        export SSHPASS=apc
        case "$action" in
            status)
                # use apc-telnet-olstatus.exp if ssh is a problem
                exp=apc-olstatus.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "^$socket")
                echo "$result"
                ;;
            off)
                # use apc-telnet-oloff.exp if ssh is a problem
                exp=apc-oloff.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "^$socket")
                echo "$result"
                ;;
            on)
                # use apc-telnet-olon.exp if ssh is a problem
                exp=apc-olon.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "^$socket")
                echo "$result"
                ;;
        esac
    fi
    if [ "$driver" = "ServerTech" ]; then
        export SSHPASS=admn
        case "$action" in
            status)
                exp=servertech-status.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "$socket")
                echo "$result"
                ;;
            off)
                exp=servertech-off.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "$socket")
                echo "$result"
                ;;
            on)
                exp=servertech-on.exp
                # fix the path later. For now run in directory
                result=$(./$exp $pdu $socket | egrep "$socket")
                echo "$result"
                ;;
        esac
    fi
done
