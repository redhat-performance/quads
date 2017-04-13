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

# pass arguments : e.g. 2016-11 30
YEAR_MONTH=$1
YEAR=$(echo $YEAR_MONTH | awk -F- '{ print $1 }')
MONTH=$(echo $YEAR_MONTH | awk -F- '{ print $2 }')
NUM_DAYS=$2

$quads --ls-hosts  > $TMPHOSTFILE

$bindir/simple-table-generator.py --host-file $TMPHOSTFILE -m $MONTH -y $YEAR -d $NUM_DAYS --gentime "Allocation Map for $YEAR_MONTH"
rm -f $TMPCOLORFILE $TMPHOSTFILE
