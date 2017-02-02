#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

sleep 10

data_dir=${quads["data_dir"]}
quads=${quads["install_dir"]}/bin/quads.py
foreman_param=${quads["foreman_director_parameter"]}
lockdir=$data_dir/lock

[ ! -d $lockdir ] && mkdir -p $lockdir
  
PIDFILE=$lockdir/quads-move.pid
  
if [ -f $PIDFILE ]; then
    if [ -d /proc/$(cat $PIDFILE) ]; then
        echo Another instance already running. Try again later.
        exit 1
    fi
fi

echo $$ > $PIDFILE

if [ ! -d $data_dir/boot ]; then
    mkdir $data_dir/boot
fi

if [ ! -d $data_dir/bootstate ]; then
    mkdir $data_dir/bootstate
fi

for h in $(hammer host list --search params.${foreman_param}=true | grep redhat.com  | awk '{ print $3 }' ) ; do
    if [ -f $data_dir/bootstate/$h ]; then
        current_state=$(cat $data_dir/bootstate/$h)
        if [ "$current_state" != "director" ]; then
            build_state=$(hammer host info --name $h | grep Build | awk '{ print $NF }')
            if [ "$build_state" = "no" ]; then
                echo director > $data_dir/boot/$h
            fi
        fi
    fi
done

for h in $(hammer host list --search params.${foreman_param}=false | grep redhat.com  | awk '{ print $3 }' ) ; do
    if [ -f $data_dir/bootstate/$h ]; then
        current_state=$(cat $data_dir/bootstate/$h)
        if [ "$current_state" != "foreman" ]; then
            build_state=$(hammer host info --name $h | grep Build | awk '{ print $NF }')
            if [ "$build_state" = "no" ]; then
                echo foreman > $data_dir/boot/$h
            fi
        fi
    fi
done

