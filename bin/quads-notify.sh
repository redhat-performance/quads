#!/bin/sh
#  Send email and IRC notifications when hosts are assigned
#  Send email notifications when hosts are expiring.
#######

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

# load the ../conf/quads.yml values as associative array
source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads.py
data_dir=${quads["data_dir"]}

days="1 3 5 7"

# only worry about environments with active hosts
env_list=$($quads --summary | awk '{ print $1 }')

function craft_initial_message() {
    msg_file=$(mktemp /tmp/msgXXXXXXXXXX)
    owner=$1
    env_to_report=$2
    ircbot_ipaddr=${quads["ircbot_ipaddr"]}
    ircbot_port=${quads["ircbot_port"]}
    report_file=${env_to_report}-${owner}-initial-$($quads --ls-ticket --cloud-only ${env_to_report})
    if [ ! -f ${data_dir}/report/${report_file} ]; then
        touch ${data_dir}/report/${report_file}
        if ${quads["email_notify"]} ; then
            cat > $msg_file <<EOF
To: $owner@${quads["domain"]}
Cc: ${quads["report_cc"]}
Subject: New QUADS Assignment Allocated
From: QUADS <quads@${quads["domain"]}>
Reply-To: dev-null@${quads["domain"]}

Greetings Citizen,

You've been allocated a new environment!

   $env_to_report

(Details)
http://${quads["wp_wiki"]}/assignments/#$env_to_report

You can view your machine list, duration and other
details above.

DevOps Team

EOF
            /usr/sbin/sendmail -t < $msg_file 1>/dev/null 2>&1
        fi
        if ${quads["irc_notify"]} ; then
            # send IRC notification
            echo "QUADS: $env_to_report is now active - http://${quads["wp_wiki"]}/assignments/#$env_to_report" | nc -w 1 $ircbot_ipaddr $ircbot_port

        fi
    fi
    rm -f $msg_file
}
 
function craft_message() {

    msg_file=$(mktemp /tmp/msgXXXXXXXXXX)

    owner=$1
    days_to_report=$2
    env_to_report=$3

    report_file=${env_to_report}-${owner}-${days_to_report}-$($quads --ls-ticket --cloud-only ${env_to_report})
    if [ ! -f ${data_dir}/report/${report_file} ]; then
        touch ${data_dir}/report/${report_file}
        if ${quads["email_notify"]} ; then
            cat > $msg_file <<EOF
To: $owner@${quads["domain"]}
Cc: ${quads["report_cc"]}
Subject: QUADS upcoming expiration notification
From: QUADS <quads@${quads["domain"]}>
Reply-To: dev-null@${quads["domain"]}

This is a message to alert you that in $days_to_report days
your allocated environment:

   $env_to_report

(Details)
http://${quads["wp_wiki"]}/assignments/#$env_to_report

will have some or all of the hosts expire.  The hosts in your
environment will automatically be reprovisioned and returned to
the pool of available hosts.

Thank you for your attention.

DevOps Team

EOF
            /usr/sbin/sendmail -t < $msg_file 1>/dev/null 2>&1
        fi
    fi
    rm -f $msg_file
}

for e in $env_list ; do
    craft_initial_message $($quads --cloud-only $e --ls-owner) $e
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
