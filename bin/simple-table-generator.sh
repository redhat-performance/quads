#!/bin/sh
# wrapper around simple-table-generator.py
# this generates a visualization map image of allocations across a month

# print usage if not specified
if [[ $# -ne 2 ]]; then
        echo "USAGE: ./simple-table-generator.sh YEAR-MONTH NUMBEROFDAYS"
        echo "       ./simple-table-generator.sh 2016-11 30"
	echo "                                          "
	exit 1
fi

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin

TMPHOSTFILE=$(mktemp /tmp/quadshostfileXXXXXXX)
TMPCOLORFILE=$(mktemp /tmp/quadshostcolorfileXXXXXXX)

# pass arguments : e.g. 2016-11 30
YEAR_MONTH=$1
NUM_DAYS=$2

$quads --ls-hosts  > $TMPHOSTFILE

# create and fill csv template for all hosts schedules in target timeframe
(
for h in $(cat $TMPHOSTFILE) ; do
    for i in $(seq -w 1 $NUM_DAYS) ; do
        echo -n $($quads --host $h --date "${YEAR_MONTH}-$i 08:00" | sed 's/cloud//')
        if [ $i -lt $NUM_DAYS ]; then
            echo -n ,
        else
            echo ""
        fi
    done
done
) > $TMPCOLORFILE

$bindir/simple-table-generator.py --host-file $TMPHOSTFILE --host-color-file $TMPCOLORFILE -d $NUM_DAYS
rm -f $TMPCOLORFILE $TMPHOSTFILE
