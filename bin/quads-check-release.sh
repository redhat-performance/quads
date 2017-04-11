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

function validate_environment() {
    env=$1
    owner=$2
    ticket=$3

    if $bin_dir/quads-post-network-test.sh -c $env -2 ; then
        touch $data_dir/release/${env}-${owner}-${ticket}
    fi
    return
}

for env in $($quads --summary | awk '{ print $1 }') ; do
    owner=$($quads --ls-owner --cloud-only $env)
    ticket=$($quads --ls-ticket --cloud-only $env)

    if [ "$owner" != "nobody" ]; then
        if [ ! -f $data_dir/release/${env}-${owner}-${ticket} ]; then
            validate_environment $env $owner $ticket
        fi
    fi
done
