#!/bin/sh
# This queries QUADS to determine the next
# set of changes needing to take place.
# Usage: bin/quads-change-list.sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
maxdays="183"

function quads_next_change() {
    n=0 ;
    while [ $($quads --move-hosts --dry-run --date \
                     "$(date -d "today + $n days" \
                     +"%Y-%m-%d 05:00")" | wc -l) -eq 0 ] ; do

        n=$(expr $n + 1)
        if [ $n -gt $maxdays ]; then
            echo "Exceeded the configured max days to search."
            exit 0
        fi
    done
    echo "Next change in $n days"
    date -d "today + $n days" +"%Y-%m-%d 05:00"
    $quads --move-hosts --dry-run --date "$(date -d "today + $n days" +"%Y-%m-%d 05:00")"
}

quads_next_change
