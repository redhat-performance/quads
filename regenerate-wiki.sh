#!/bin/sh
# This calls the two wrappers to generate wiki page and ownership page

tmpfile=$(mktemp /tmp/wikimarkdownXXXXX)
lockfile=/root/.wiki_regenerate

# change this to your script location 
cd /root/git/ops-tools/lab-scheduler

if [ -f $lockfile ]; then
    exit 0
else
    touch $lockfile
    # generate racks wiki page
    sh create-input.sh 1>$tmpfile  2>&1
    ./racks-wiki.py --markdown $tmpfile --wp-url http://wiki.example.com/xmlrpc.php --wp-username admin --wp-password admin --page-title "Title of your Dashboard" --page-id 4
    # generate assignments and ownership page
    sh create-input-assignments.sh 1>$tmpfile  2>&1
    ./racks-wiki-ownership.py --markdown $tmpfile --wp-url http://wiki.example.com/xmlrpc.php --wp-username admin --wp-password admin --page-title "Title of your Systems Ownership Page" --page-id 357
rm -f $tmpfile $lockfile
fi
