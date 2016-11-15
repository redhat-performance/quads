#!/bin/sh
#
#  Send notifications when hosts are expiring.
#
#######

quads=/root/schedule.py

days="1 3 5 7"
#days="14 21 25 27"

# only worry about environments with active hosts
env_list=$($quads --summary | awk '{ print $1 }')

function craft_message() {

    msg_file=$(mktemp /tmp/msgXXXXXXXXXX)

    owner=$1
    days_to_report=$2
    env_to_report=$3

    report_file=${env_to_report}-${owner}-${days_to_report}-$($quads --ls-ticket --cloud-only ${env_to_report})
    if [ ! -f /etc/lab/report/${report_file} ]; then
        touch /etc/lab/report/${report_file}
        cat > $msg_file <<EOF
To: $owner@example.com
Cc: someuser@example.com, someuser@example.com, someuser@example.com, someuser@example.com
Subject: QUADS upcoming expiration notification
From: QUADS <quads@example.com>
Reply-To: dev-null@example.com

This is a message to alert you that in $days_to_report days
your allocated environment:

   $env_to_report

(Details)
http://wiki.example.com/assignments/#$env_to_report

will have some or all of the hosts expire.  The hosts in your
environment will automatically be reprovisioned and returned to
the pool of available hosts.

Thank you for your attention.

Scale/Perf DevOps Team

EOF
        /usr/sbin/sendmail -t < $msg_file 1>/dev/null 2>&1
    fi
    rm -f $msg_file
}

for e in $env_list ; do
    alerted=false
    for d in $days ; do
        # if "nobody" is the owner you can skip it...
        if [ "$($quads --ls-owner --cloud-only $e)" == "nobody" ]; then
            :
        else
            if $alerted ; then
                :
            else
                current_count=$($quads --cloud-only $e --date "$(date +%Y-%m-%d) 00:00" | wc -l)
                upcoming_count=$($quads --cloud-only $e --date "$(date -d "now + $d days" +%Y-%m-%d) 00:00" | wc -l)
                if [ $upcoming_count -lt $current_count ]; then
                    craft_message $($quads --cloud-only $e --ls-owner) $d $e
                    alerted=true
                fi
            fi
        fi
    done
done
