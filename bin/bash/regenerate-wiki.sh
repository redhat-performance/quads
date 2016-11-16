#!/bin/sh

lockfile=/root/.wiki_regenerate

if [ -f $lockfile ]; then
    if [ -d /proc/$(cat $lockfile) ]; then
        exit 0
    else
        echo $$ > $lockfile
    fi
else
    echo $$ > $lockfile
fi


tmpfile=$(mktemp /tmp/wikimarkdownXXXXX)

cd /root/ops-tools/lab-scheduler

sh create-input.sh 1>$tmpfile  2>&1
./racks-wiki.py --markdown $tmpfile --wp-url http://wiki.example.com/xmlrpc.php --wp-username  ADMINUSER --wp-password  ADMINPASSWORD --page-title "RDU ScaleLab Dashboard"
sh create-input-assignments.sh 1>$tmpfile  2>&1
./racks-wiki.py --markdown $tmpfile --wp-url http://wiki.example.com/xmlrpc.php --wp-username  ADMINUSER --wp-password  ADMINPASSWORD --page-title "assignments" --page-id 357
rm -f $tmpfile $lockfile

