#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
data_dir=${quads["data_dir"]}
bindir=${quads["install_dir"]}/bin
toolsdir=${quads["install_dir"]}/lib/tools
wp_wiki=${quads["wp_wiki"]}
wp_username=${quads["wp_username"]}
wp_password=${quads["wp_password"]}
wp_wiki_main_title=${quads["wp_wiki_main_title"]}
wp_wiki_main_page_id=${quads["wp_wiki_main_page_id"]}
wp_wiki_assignments_title=${quads["wp_wiki_assignments_title"]}
wp_wiki_assignments_page_id=${quads["wp_wiki_assignments_page_id"]}
wp_wiki_git_manage=${quads["wp_wiki_git_manage"]}
wp_wiki_git_repo_path=${quads["wp_wiki_git_repo_path"]}


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
if $wp_wiki_git_manage ; then
    if [ ! -d $wp_wiki_git_repo_path ]; then
        exit 1
    fi
    cp $tmpfile $wp_wiki_git_repo_path/main.md
    pushd $wp_wiki_git_repo_path
    git commit -a -m "$(date) content update"
    export PAGER=cat
    GITDIFF="$(git diff origin/master)"
    if [ -z "$GITDIFF" ]; then
        :
    else
        $toolsdir/racks_wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_main_title" --page-id $wp_wiki_main_page_id
        git push
    fi
    popd
else
    $toolsdir/racks_wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_main_title" --page-id $wp_wiki_main_page_id
fi
$bindir/create-input-assignments.sh 1>$tmpfile  2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
if grep -q Traceback $tmpfile ; then
    exit 1
fi
if $wp_wiki_git_manage ; then
    if [ ! -d $wp_wiki_git_repo_path ]; then
        exit 1
    fi
    cp $tmpfile $wp_wiki_git_repo_path/assignments.md
    pushd $wp_wiki_git_repo_path
    git commit -a -m "$(date) content update"
    export PAGER=cat
    GITDIFF="$(git diff origin/master)"
    if [ -z "$GITDIFF" ]; then
        :
    else
        $toolsdir/racks_wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_assignments_title" --page-id $wp_wiki_assignments_page_id
        git push
    fi
    popd
else
    $toolsdir/racks_wiki.py --markdown $tmpfile --wp-url http://$wp_wiki/xmlrpc.php --wp-username  $wp_username --wp-password  $wp_password --page-title "$wp_wiki_assignments_title" --page-id $wp_wiki_assignments_page_id
fi
rm -f $tmpfile $lockfile

