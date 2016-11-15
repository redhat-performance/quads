#!/bin/sh

# takes two arguments.
#   Number of nodes
#   Number of days

nodes=$1
days=$2

listfile=$(mktemp /root/tmp/hostfileXXXXXXX)
combofile=$(mktemp /root/tmp/combosXXXXXXX)
hostset=$(mktemp /root/tmp/hostsetXXXXXX)

# print usage if not specified
if [[ $# -ne 2 ]]; then
        echo "USAGE: ./find-available.sh NUMBER_OF_NODES NUMBER_OF_DAYS"
    echo "EXAMPLE: ./find-available.sh 10 20"
    echo "                                      "
    exit 1
fi

function avail_for() {
    start_day=$1
    n=$2
    duration=$3

    /root/schedule.py --cloud-only cloud01 --date "$(date -d "today + $start_day days" +"%Y-%m-%d 08:00")" > $listfile
    /root/sample.py  --input $listfile --count $n > $combofile

    cat $combofile | while read set ; do
#    for set in $(cat $combofile) ; do
        fail=false
        for h in $(echo $set | sed 's/,/ /g') ; do
            for t in $(seq $start_day $(expr $start_day + $duration)) ; do
                if [ $(/root/schedule.py --host $h --date "$(date -d "today + $t days" '+%Y-%m-%d 08:00')") != cloud01 ]; then
                    fail=true
                fi
            done
            if ! $fail ; then
                echo $set > $hostset
                echo 0
                return
            fi
        done
    done
    echo 1
    return
}

function find_date() {
    node_count=$1
    for_days=$2

    count=0
    increment=0
    # keep moving forward in time until you find what you need ...
    while [ $count -lt $node_count -a $(avail_for $increment $node_count $for_days) -ne 0 ]; do
        count=$(/root/schedule.py --full-summary --date "$(date -d "today + $increment days" '+%Y-%m-%d 08:00')" | grep cloud01 | awk '{ print $3 }')
        if [ $count -lt $node_count ]; then
            increment=$(expr $increment + 1)
        fi
    done
    echo $increment
}

# this is where things start ...
first_avail=$(find_date $nodes $days)

echo First available date for : $nodes nodes for $days days is 
echo "     $(date -d "today + $first_avail days" '+%Y-%m-%d 08:00')"
echo Host list:
for h in $(cat $hostset | sed 's/,/ /g') ; do
    echo "     "$h
done

rm -f $listfile $combofile $hostset
