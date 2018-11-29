#!/bin/sh
#
# Checks the environment to make sure it can be
# released to the end user.  Currently one test is
# being run (the post network test).  This can be
# extended as more pre-notification checks are deemed
# necessary.  Other possible checks would be to
# validate PXE boot order.

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
install_dir=${quads["install_dir"]}
bin_dir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
report_cc=${quads["report_cc"]}
gather_ansible_facts=${quads["gather_ansible_facts"]}
gather_dell_configs=${quads["gather_dell_configs"]}
json_web_path=${quads["json_web_path"]}
# if failure persiste beyond tolerance, do reporting.
tolerance=14400

function report_failure() {
    env=$1
    owner=$2
    ticket=$3
    resultfile=$4
    msgfile=$(mktemp /tmp/reportFailXXXXXXX)
    cat > $msgfile <<EOM
To: $report_cc
Subject: Validation check failed for $env / $owner / $ticket
From: QUADS <quads@${quads["domain"]}>
Reply-To: dev-null@${quads["domain"]}

A post allocation test has failed for:

   cloud: $env
   owner: $owner
   ticket: $ticket

The release of the environment is contingent on the success
of the validation scripts.  Before users are notified, make
sure to address the environment and ensure all validation steps
succeed to ensure a timely release to the end user.

DevOps Team

EOM
    echo "Results:" >> $msgfile
    cat $resultfile >> $msgfile
    /usr/sbin/sendmail -t < $msgfile 1>/dev/null 2>&1
    if [ ${quads["elastic_stats_enabled"]} ]; then
      ${bin_dir}/index-data.py --resultfile $resultfile --index validation-errors --type validation-log --owner $owner --ticket $ticket --cloud $env
    fi
    rm -f $msgfile
}

function report_success() {
    env=$1
    owner=$2
    ticket=$3
    msgfile=$(mktemp /tmp/reportFailXXXXXXX)
    cat > $msgfile <<EOM
To: $report_cc
Subject: Validation check succeeded for $env / $owner / $ticket
From: QUADS <quads@${quads["domain"]}>
Reply-To: dev-null@${quads["domain"]}

A post allocation check previously failed for:

   cloud: $env
   owner: $owner
   ticket: $ticket

has successfully passed the verification test(s)!  The owner
should receive a notification that the environment is ready
for use.

DevOps Team

EOM
    /usr/sbin/sendmail -t < $msgfile 1>/dev/null 2>&1
    rm -f $msgfile
}

function env_allocation_time_exceeded() {
    env=$1

    first_host=$($quads --cloud-only $env | head -1)
    start_time=$($quads --ls-schedule --host $first_host | grep $env | tail -1 | sed 's/.*start=\(.*\),end=.*/\1/')
    if [ $(expr $(date +%s) - $(date -d "$start_time" +%s)) -gt $tolerance ]; then
        return 0
    else
        return 1
    fi
}

function validate_environment() {
    env=$1
    owner=$2
    ticket=$3
    resultfile=$(mktemp /tmp/netcheckXXXXXXX)

    if $bin_dir/quads-post-system-test.py --cloud $env 1>$resultfile 2>&1; then
        :
    else
        if env_allocation_time_exceeded $env ; then
            if [ ! -f $data_dir/release/.failreport.${env}-${owner}-${ticket} ]; then
                report_failure $env $owner $ticket $resultfile
                cat $resultfile > $data_dir/release/.failreport.${env}-${owner}-${ticket}
            fi
        fi
        rm -f $resultfile
        return
    fi

    if [ "${gather_ansible_facts}" == "true" ]; then
        if $bin_dir/quads-ansible-cmdb-facts.sh $env $owner $ticket 1>/dev/null 2>&1 ; then
            :
        else
            if env_allocation_time_exceeded $env ; then
                echo "Something went wrong with ansible-cmdb for ${env}-${owner}-${ticket}" > $resultfile
                if [ ! -f $data_dir/release/.failreport.${env}-${owner}-${ticket} ]; then
                    report_failure $env $owner $ticket $resultfile
                    cat $resultfile > $data_dir/release/.failreport.${env}-${owner}-${ticket}
                fi
            fi
            rm -f $resultfile
            return
        fi
    fi

    if $bin_dir/quads-post-network-test.sh -c $env -2 1>$resultfile 2>&1; then
        touch $data_dir/release/${env}-${owner}-${ticket}
        if [ -f $data_dir/release/.failreport.${env}-${owner}-${ticket} ]; then
            for file in $data_dir/vlans/${env}*; do
                if ! find $file &> /dev/null; then
                    report_success $env $owner $ticket
                fi;
            done
        fi
        if [ "${gather_dell_configs}" == "true" ]; then
            # now that we have success, we can also generate the dell report
            $bin_dir/quads-dell-config-report.sh $env 1> $json_web_path/${env}-${owner}-${ticket}-dellconfig.html 2>/dev/null
        fi
    else
        if env_allocation_time_exceeded $env ; then
            if [ ! -f $data_dir/release/.failreport.${env}-${owner}-${ticket} ]; then
                report_failure $env $owner $ticket $resultfile
                cat $resultfile > $data_dir/release/.failreport.${env}-${owner}-${ticket}
            fi
        fi
    fi
    rm -f $resultfile
    return
}

for env in $($quads --summary | awk '{ print $1 }') ; do
    owner=$($quads --ls-owner --cloud-only $env)
    ticket=$($quads --ls-ticket --cloud-only $env)

    if [ "$owner" != "nobody" -a "$owner" -a "$ticket" ]; then
        if [ ! -f $data_dir/release/${env}-${owner}-${ticket} ]; then
            validate_environment $env $owner $ticket
        fi
    fi
done
