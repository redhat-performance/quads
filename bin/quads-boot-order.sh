#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
install_dir=${quads["install_dir"]}
bin_dir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}

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

    if [ -f $install_dir/ansible/racadm-setup-boot-${host_type}-${playbook_type}.yml ] ; then
        playbook=$install_dir/ansible/racadm-setup-boot-${host_type}-${playbook_type}.yml
    else
        return
    fi
    host_inventory=$(mktemp /tmp/hostfileXXXXXX)
    echo mgmt-$target > $host_inventory

    PIDFILE=$data_dir/ansible/$target

    if [ -f $PIDFILE ]; then
        if [ -d /proc/$(cat $PIDFILE) ]; then
            echo Another instance already running. Try again later.
            rm -f $host_inventory
            exit 1
        fi
    fi

    echo ============ starting ansible @ $(date) >> /var/log/quads/$target 2>&1
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

for h in $($quads --ls-hosts) ; do
    if [ -f $data_dir/boot/$h ]; then
        reconfigure $h
    fi
done

