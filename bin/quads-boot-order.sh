#!/bin/sh
# This is only used for Dell servers that require toggling
# the PXE flag and interface order on the provisioning
# interface to accomodate # OpenStack Directory-deployed clouds.
# Other server types may require something similiar if they have
# more advanced out-of-band boot orderering and persistence options.
# More simple server IPMI implementations (like Supermicro) do not
# need this level of accomodation for OSP Director.
# See:
# https://github.com/redhat-performance/quads/tree/master/templates
# https://github.com/redhat-performance/quads/tree/master/ansible

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
install_dir=${quads["install_dir"]}
data_dir=${quads["data_dir"]}
ansible_max_proc=${quads["ansible_max_proc"]}

function reconfigure() {
    target=$1

    playbook_type=$(cat $data_dir/boot/$target)
    host_type=$(echo $target | awk -F. '{ print $1 }' | awk -F- '{ print $3 }')

    current_type=""
    if [ -f $data_dir/bootstate/$target ]; then
        current_type=$(cat $data_dir/bootstate/$target)
    fi

    if [ "$current_type" = "$playbook_type" ]; then
        # ensure subsequent cron does not pick this up ...
        rm -f $data_dir/boot/$target
        return
    fi

    echo '==== '$target
    echo '== checking for '$install_dir/ansible/racadm-setup-boot-${target}-${playbook_type}.yml
    if [ -f $install_dir/ansible/racadm-setup-boot-${target}-${playbook_type}.yml ]; then
        playbook=$install_dir/ansible/racadm-setup-boot-${target}-${playbook_type}.yml
    else
        echo '== checking for '$install_dir/ansible/racadm-setup-boot-${host_type}-${playbook_type}.yml
        if [ -f $install_dir/ansible/racadm-setup-boot-${host_type}-${playbook_type}.yml ] ; then
            playbook=$install_dir/ansible/racadm-setup-boot-${host_type}-${playbook_type}.yml
        else
            rm -f $data_dir/boot/$target
            echo $playbook_type > $data_dir/bootstate/$target
            return
        fi
    fi
    host_inventory=$(mktemp /tmp/hostfileXXXXXX)
    echo mgmt-$target > $host_inventory

    PIDFILE=$data_dir/ansible/$target

    # check to see if there is already a process running that is dealing with
    # boot order for this host.  If so, return.

    if [ -f $PIDFILE ]; then
        if [ -d /proc/$(cat $PIDFILE) ]; then
            if [ "$(cat /proc/$(cat $PIDFILE)/cmdline | strings -1 | grep $0)" ]; then
                echo Another instance already running. Try again later.
                rm -f $host_inventory
                return
            fi
        fi
    fi

    # safety check to avoid too many processes running at once
    if [ "$(pgrep -f ansible-playbook -c)" -gt $ansible_max_proc ]; then
        echo Too many ansible-playbook processes running.  Try again later.
        rm -f $host_inventory
        return
    fi

    echo '============ starting ansible @ '$(date) >> /var/log/quads/$target 2>&1
    # note that when you run a subshell using this construct:
    #     command1 && command2 &
    # then $! is really a fork of $0, and hence /proc/<pid>/cmdline will have
    # the same name as $0, as opposed to the backgrounded command.  e.g.
    # if this script is called quads-boot-order.sh, then when you call:
    #    ansible-playbook -i blah $playbook && echo blab blah &
    # followed by :
    #    echo $! > $PIDFILE
    # then the /proc/$(cat $PIDFILE)/cmdline will include "quads-boot-order.sh"
    # as opposed to "ansible-playook".  This is due to the && construct forcing
    # the subshell.

    ansible-playbook -i $host_inventory $playbook 1>>/var/log/quads/$target 2>&1 && echo $playbook_type > $data_dir/bootstate/$target || echo $playbook_type > $data_dir/boot/$target &
    echo $! > $PIDFILE
    sleep 60
    rm -f $host_inventory
}

if [ ! -d $data_dir/boot ]; then
    mkdir $data_dir/boot
fi

if [ ! -d $data_dir/bootstate ]; then
    mkdir $data_dir/bootstate
fi

if [ ! -d $data_dir/ansible ]; then
    mkdir $data_dir/ansible
fi

echo 'QUADS == '$quads
$quads --ls-hosts
echo ""
for h in $($quads --ls-hosts) ; do
    echo '=== MAIN : '$h
    if [ -f $data_dir/boot/$h ]; then
        reconfigure $h
    fi
done
