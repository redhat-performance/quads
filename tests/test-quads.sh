#!/bin/sh
#
############################################
# QUADS Simulator 5000
# Test quads using CI or in a sandbox.
# We use this in a Jenkins instance  with the Gerrit
# trigger plugin to be run on all patchsets.
#
# Requires: shellcheck, python-flake8
#
#  ./test-quads.sh 2>&1 | less
#
############################################

if [ -z "$1" ]; then
    cp $0 ./bin/jenkins-ci-test.sh
    chmod 755 ./bin/jenkins-ci-test.sh
    exec `pwd`/bin/jenkins-ci-test.sh recursive
fi
if [ -f /home/quads-ci/foreman ]; then
    source /home/quads-ci/foreman
fi

## Jenkins specific debug here
echo '========== START === '`date`' ===================='
echo "called as $0"
echo "called with params: $*"
printenv
echo pwd is: `pwd`
echo "------"
ls -la
echo "------"
## end Jenkins debug here

## start virtualenv
virtualenv jenkins
. jenkins/bin/activate
pip install pyaml
pip install requests
# pexpect package for machine control
pip install --pre strip

install_bin=$(dirname $0)

if [ ! -e $install_bin/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

if [ "$GERRIT_CHANGE_NUMBER" ]; then
    cat >> .git/config <<EOF
[remote "gerrit"]
url = https://review.gerrithub.io/redhat-performance/quads
fetch = +refs/heads/*:refs/remotes/origin/*
EOF
    git review -d $GERRIT_CHANGE_NUMBER
else
    echo "========= GERRIT_CHANGE_NUMBER not set ========="
    exit 0
fi

# this should show us where it is
git log --no-decorate -n 1


TMPDIR=$(mktemp -d /tmp/quadsXXXXXXX)
DATA=$TMPDIR/sample.yaml
STATEDIR=$TMPDIR/state
LOGFILE=$TMPDIR/logfile

quads="python $install_bin/quads-cli"
bindir="$(dirname $0)"
libdir=$bindir/../lib

function quads_daemon_start() {
    sed -i -e "s@quads_base_url: http://127.0.0.1:8080/@quads_base_url: http://127.0.0.1:8082/@g" $install_bin/../conf/quads.yml
    if [ ! -z "$FOREMAN_API_URL" ]; then
        sed -i -e "s@foreman_api_url: https://foreman.example.com/api/v2@foreman_api_url: $FOREMAN_API_URL@g" $install_bin/../conf/quads.yml
    fi
    if [ ! -z "$FOREMAN_PASSWORD" ]; then
        sed -i -e "s@foreman_password: password@foreman_password: $FOREMAN_PASSWORD@g" $install_bin/../conf/quads.yml
    fi
    quads_start="python $(dirname $0)/quads-daemon --config $DATA --statedir $STATEDIR --log-path $LOGFILE --port 8082"
    $quads_start  1>/dev/null 2>&1 &
}

function quads_daemon_stop() {
    pids="$(pgrep quads-daemon)"
    if [ "$pids" ]; then
	kill $pids
    fi
}

tests="
init
declare_cloud01
declare_cloud02
declare_cloud03
declare_cloud04
decl_host01
decl_host02
decl_host03
decl_host04
redefine_cloud02
ls_owner
ls_ticket
ls_hosts
ls_clouds
ls_qinq
simple
add_schedule_host04
delete_cloud02_fail
mod_schedule_host04
delete_cloud02_success
rm_schedule_host04
delete_cloud03_success
declare_cloud02
declare_cloud03
delete_host04
decl_host04
add_schedule_host04
add_schedule_host03
add_schedule2_host03
add_schedule2_host04
ls_schedule_host03
ls_schedule_host04
rm_schedule2_host04
check_move_1
check_move_2
"

declare -A quads_tests=(
    ["declare_cloud01"]="$quads --define-cloud cloud01 --description cloud01"
    ["declare_cloud02"]="$quads --define-cloud cloud02 --description cloud02 --cloud-owner bob"
    ["declare_cloud03"]="$quads --define-cloud cloud03 --description cloud03 --cloud-owner joe --cloud-ticket 12345"
    ["declare_cloud04"]="$quads --define-cloud cloud04 --description cloud04 --cloud-owner will --cloud-ticket 54321 --qinq 1"
    ["decl_host01"]="$quads --define-host host01.example.com --default-cloud cloud01 --host-type vendor"
    ["decl_host02"]="$quads --define-host host02.example.com --default-cloud cloud01 --host-type vendor"
    ["decl_host03"]="$quads --define-host host03.example.com --default-cloud cloud01 --host-type vendor"
    ["decl_host04"]="$quads --define-host host04.example.com --default-cloud cloud01 --host-type vendor"
    ["redefine_cloud02"]="$quads --define-cloud cloud02 --description cloud02_redefined --cloud-owner wfoster --force"
    ["ls_owner"]="$quads --ls-owner"
    ["ls_ticket"]="$quads --ls-ticket"
    ["ls_hosts"]="$quads --ls-hosts"
    ["ls_clouds"]="$quads --ls-clouds"
    ["ls_qinq"]="$quads --ls-qinq"
    ["simple"]="$quads"
    ["add_schedule_host04"]="$quads --add-schedule --host host04.example.com --schedule-start \"2016-01-01 08:00\" --schedule-end \"2016-01-10 08:00\" --schedule-cloud cloud02"
    ["delete_cloud02_fail"]="$quads --rm-cloud cloud02"
    ["mod_schedule_host04"]="$quads --mod-schedule 0 --host host04.example.com --schedule-end \"2016-01-15 08:00\" --schedule-cloud cloud03"
    ["delete_cloud02_success"]="$quads --rm-cloud cloud02"
    ["rm_schedule_host04"]="$quads --rm-schedule 0 --host host04.example.com"
    ["delete_cloud03_success"]="$quads --rm-cloud cloud03"
    ["delete_host04"]="$quads --rm-host host04.example.com"
    ["add_schedule_host03"]="$quads --add-schedule --host host03.example.com --schedule-start \"2016-01-01 08:00\" --schedule-end \"2016-01-10 08:00\" --schedule-cloud cloud02"
    ["add_schedule2_host03"]="$quads --add-schedule --host host03.example.com --schedule-start \"2016-01-10 08:00\" --schedule-end \"2016-01-20 08:00\" --schedule-cloud cloud02"
    ["add_schedule2_host04"]="$quads --add-schedule --host host04.example.com --schedule-start \"2016-01-10 08:00\" --schedule-end \"2016-01-20 08:00\" --schedule-cloud cloud02"
    ["ls_schedule_host03"]="$quads --ls-schedule --host host03.example.com"
    ["ls_schedule_host04"]="$quads --ls-schedule --host host04.example.com"
    ["rm_schedule2_host04"]="$quads --rm-schedule 1 --host host04.example.com"
    ["check_move_1"]="$quads --move-hosts --dry-run --date \"2016-01-02 09:00\""
    ["check_move_2"]="$quads --move-hosts --dry-run --date \"2016-01-12 09:00\""
    )

echo '====== Starting quads-daemon service on TCP/8082 : '$TMPDIR

quads_daemon_start

echo '====== Initializing sample data in :  '$TMPDIR

for test in $tests ; do
  action="${quads_tests[$test]}"
  echo '====================================='
  echo running test \"$test\": $action
  eval $action
  retvalue=$?
  if [ $retvalue -ne 0 ]; then
      echo "Failed test: $test"
      quads_daemon_stop
      exit $retvalue
  fi
  echo ------ current data ------
  cat $DATA
done
rm -rf $TMPDIR

echo '====== Stopping quads-daemon service'

quads_daemon_stop

echo '====== Initializing shellcheck with style-related exclusions'

shellcheck $bindir/*.sh --exclude=SC1068,SC2086,SC2046,SC2143,SC1068,SC2112,SC2002,SC2039,SC2155,SC2015,SC2012,SC2013,SC2034,SC2006,SC2059,SC2148,SC2154,SC2121,SC2154,SC2028,SC2003,SC2035,SC2005,SC2027,SC2018,SC2019,SC2116

if [ "$?" = "0" ]; then
   :
else
   echo "FATAL error with one of the shell tools"
   exit 1
fi

echo '====== Initializing flake8 Python tests with style-related exclusions'

# primary python tools
flake8 $bindir/*.py --ignore=F401,E302,E226,E231,E501,E225,E402,F403,F999,E127,W191,E101,E711,E201,E202,E124,E203,E122,E111,E128,E116,E222
# now we include libdir as well
flake8 $libdir/*.py --ignore=F401,E302,E226,E231,E501,E225,E402,F403,F999,E127,W191,E101,E711,E201,E202,E124,E203,E122,E111,E128,E116,E222
# individual checks for daemon and client
flake8 $bindir/quads-daemon --ignore=F401,E302,E226,E231,E501,E225,E402,F403,F999,E127,W191,E101,E711,E201,E202,E124,E203,E122,E111,E128,E116,E222
flake8 $bindir/quads-cli --ignore=F401,E302,E226,E231,E501,E225,E402,F403,F999,E127,W191,E101,E711,E201,E202,E124,E203,E122,E111,E128,E116,E222

if [ "$?" = "0" ]; then
    :
else
    echo "FATAL error with one of the Python tools"
    exit 1
fi

## Jenkins post data here
echo '========== FINISH == '`date`' ===================='

exit 0
## end Jenkins post data here
