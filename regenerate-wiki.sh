#!/bin/sh

tmpfile=$(mktemp /tmp/wikimarkdownXXXXX)
lockfile=/root/.wiki_regenerate

# change this to your script location 
cd /root/git/ops-tools/lab-scheduler

if [ -f $lockfile ]; then
    exit 0
else
    touch $lockfile
    sh create-input.sh 1>$tmpfile  2>&1
    ./racks-wiki.py --markdown $tmpfile --wp-url http://wiki.example.com/xmlrpc.php --wp-username admin --wp-password admin --page-title "Title of your Dashboard"
    rm -f $tmpfile $lockfile
fi

