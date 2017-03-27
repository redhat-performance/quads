#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
data_dir=${quads["data_dir"]}
bindir=${quads["install_dir"]}/bin
wp_wiki=${quads["wp_wiki"]}
wp_username=${quads["wp_username"]}
wp_password=${quads["wp_password"]}
wp_wiki_main_title=${quads["wp_wiki_main_title"]}
wp_wiki_main_page_id=${quads["wp_wiki_main_page_id"]}
wp_wiki_assignments_title=${quads["wp_wiki_assignments_title"]}
wp_wiki_assignments_page_id=${quads["wp_wiki_assignments_page_id"]}


lockfile=$data_dir/.wiki_regenerate

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

$bindir/create-input.sh 1>$tmpfile  2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
if grep -q Traceback $tmpfile ; then
    exit 1
fi
$bindir/racks-wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_main_title" --page-id $wp_wiki_main_page_id
$bindir/create-input-assignments.sh 1>$tmpfile  2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
if grep -q Traceback $tmpfile ; then
    exit 1
fi
$bindir/racks-wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_assignments_title" --page-id $wp_wiki_assignments_page_id
rm -f $tmpfile $lockfile

