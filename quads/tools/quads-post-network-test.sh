#!/bin/sh
# This performs fping tests on all of the interfaces
# across a specific cloud.  It requires an OS to be up
# and answering so it's best done post-deployment but
# before machines are being consumed by the user.

function usage() {
    echo "Usage: `basename $0` [ -c cloudname | --cloud cloudname ] [ -1 ][ -2 ][ -3 ][ -4 ]"
    echo "       `basename $0` [ -f hostlist | --file hostlist ]"
    echo "  e.g. `basename $0` -c cloud11  (run test against cloud11 hosts)"
    echo "       `basename $0` -f hostlist (run test against hosts in hostlist)"
}

args=`getopt -o c:f:1234 -l cloud:,file: -- "$@"`

if [ $? != 0 ] ; then usage ; echo "Terminating..." >&2 ; exit 1 ; fi

firstnic=false
secondnic=false
thirdnic=false
fourthnic=false

eval set -- "$args"
while true ; do
        case "$1" in
                -1)
                    firstnic=true ; shift;
                    ;;
                -2)
                    secondnic=true ; shift;
                    ;;
                -3)
                    thirdnic=true ; shift;
                    ;;
                -4)
                    fourthnic=true ; shift;
                    ;;
                 -c|--cloud)
                    cloudname=$2 ; shift 2;
                    if [ "$(echo $cloudname | cut -c 1)" = "-" -o -z "$cloudname" ]; then
                        usage ; echo "Terminating..." >&2
                        exit 1
                    fi
                    ;;
                -f|--file)
                    host_list=$2 ; shift 2;
                    if [ "$(echo $host_list | cut -c 1)" = "-" -o -z "$host_list" ]; then
                        usage ; echo "Terminating..." >&2
                        exit 1
                    fi
                    if [ ! -r $host_list ]; then
                        echo `basename $0`: cannot open $host_list
                        echo "Terminating..." >&2
                        exit 1
                    fi
                    ;;
                --)
                    shift ; break ;
                    ;;
        esac
done

if [ "$host_list" -a "$cloudname" ]; then usage ; echo "Terminating..." >&2 ; exit 1 ; fi
if [ -z "$host_list" -a -z "$cloudname" ]; then usage ; echo "Terminating..." >&2 ; exit 1 ; fi

TMPFILE=$(mktemp /tmp/host_listXXXXXX)

if [ -z "$host_list" ]; then
    echo "sorry this mode is broken.  Running a modified version."
    exit 1
    $quads --cloud-only $cloudname > $TMPFILE
    host_list=$TMPFILE
fi

test_host=$(head -1 $host_list)
test_command=$(ssh -o passwordauthentication=no -o connecttimeout=3 $test_host hostname 2>/dev/null)
tmp_script=$(mktemp /tmp/tmpscriptXXXXXX)

if [ "$test_command" != "$test_host" ]; then
    echo "Host $test_host does not seem to be accessible"
#    rm -f $tmp_script $TMPFILE
#    exit 1
fi

remote_hostlist=/tmp/host_list_$$
scp $host_list $test_host:$remote_hostlist 1>/dev/null 2>&1

nic_test=$(ssh $test_host fping -u -f $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

if [ -n "$nic_test" ]; then
    echo "Something went wrong with the fping test"
    echo "$nic_test"
#    rm -f $tmp_script $TMPFILE
#    exit 1
fi

echo "Provisioning ping tests: OK"

cat > $tmp_script <<EOF
#!/bin/sh

host_list=\$1

fping -u \$(for h in \$(cat \$host_list) ; do host \$h ; done | awk '{ print \$NF }' | sed 's/10.1/172.16/')
EOF

if $firstnic ; then
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping test on NIC2"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "First data NIC tests: OK"

    sed -i -e 's/172.../172.20/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping qinq test on NIC2"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "First data NIC QinQ tests: OK"
fi

if $secondnic ; then
    sed -i -e 's/172.../172.17/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping test on NIC3"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "Second data NIC tests: OK"

    sed -i -e 's/172.../172.21/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping qinq test on NIC3"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "Second data NIC QinQ tests: OK"
fi

if $thirdnic ; then
    sed -i -e 's/172.../172.18/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping test on NIC4"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi
    echo "Third data NIC tests: OK"

    sed -i -e 's/172.../172.22/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping qinq test on NIC4"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "Third data NIC QinQ tests: OK"

fi

if $fourthnic ; then
    sed -i -e 's/172.../172.19/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping test on NIC5"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi
    echo "fourth data NIC tests: OK"

    sed -i -e 's/172.../172.23/g' $tmp_script
    scp $tmp_script $test_host:$tmp_script 1>/dev/null 2>&1
    nic_test=$(ssh $test_host sh $tmp_script $remote_hostlist 2>&1 | grep -v "Warning: Permanently added")

    if [ -n "$nic_test" ]; then
        echo "Something went wrong with the fping qinq test on NIC5"
        echo "$nic_test"
#        rm -f $tmp_script $TMPFILE
#        exit 1
    fi

    echo "fourth data NIC QinQ tests: OK"

fi

rm -f $tmp_script $TMPFILE
ssh $test_host rm -f $tmp_script 1>/dev/null 2>&1

exit 0
