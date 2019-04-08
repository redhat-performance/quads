#!/usr/bin/sh
# For existing shell scripts to use the ../conf/quads.yml
# this helper function is included.  Ultimately the use
# of shell scripts will be depricated.

function load_data() {
    if [ ! -e $(dirname $0)/yay.sh ]; then
        echo "$(basename $0): could not find yay.sh"
        exit 1
    fi

    source $(dirname $0)/yay.sh

    if [ ! -e $(dirname $0)/../conf/quads.yml ]; then
        echo "$(basename $0): could not find $(dirname $0)/../conf/quads.yml"
        exit 1
    fi

    yay $(dirname $0)/../conf/quads.yml
}

load_data
