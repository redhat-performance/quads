#!/bin/sh
#
# Adapted example/test-quads.sh to be able to run in local environment (without gerrit change number or jenkins instance) 
#  
# To run:
#
#   (don't type '$' - I just put that in to represent the command prompt)
#
#   First copy into the bin folder in your quads repo:
#   $ cp ./test-quads-local.sh /your/path/to/quads/bin/
#   
#   Then change to that directory, and execute script
#   $ cd /your/path/to/quads/bin/
#   $ ./test-quads-local.sh
# 
# As the test generates a lot of output, if you want to scroll through it at your own pace, you might want to pipe the output to a file:
#   $ ./test-quads-local.sh > output.txt
#   $ less output.txt
#
############################################




TMPDIR=$(mktemp -d /tmp/quadsXXXXXXX)
DATA=$TMPDIR/sample.yaml
STATEDIR=$TMPDIR/state
quads="python $(dirname $0)/../bin/quads.py --config $DATA --statedir $STATEDIR"

tests="
init
declare_cloud01
declare_cloud02
declare_cloud03
decl_host01
decl_host02
decl_host03
decl_host04
redefine_cloud02
ls_owner
ls_ticket
ls_hosts
ls_clouds
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
sync_state
check_move_1
check_move_2
"

declare -A quads_tests=(
    ["init"]="$quads --init"
    ["declare_cloud01"]="$quads --define-cloud cloud01 --description cloud01"
    ["declare_cloud02"]="$quads --define-cloud cloud02 --description cloud02 --cloud-owner bob"
    ["declare_cloud03"]="$quads --define-cloud cloud03 --description cloud03 --cloud-owner joe --cloud-ticket 12345"
    ["decl_host01"]="$quads --define-host host01.example.com --default-cloud cloud01"
    ["decl_host02"]="$quads --define-host host02.example.com --default-cloud cloud01"
    ["decl_host03"]="$quads --define-host host03.example.com --default-cloud cloud01"
    ["decl_host04"]="$quads --define-host host04.example.com --default-cloud cloud01"
    ["redefine_cloud02"]="$quads --define-cloud cloud02 --description cloud02_redefined --cloud-owner wfoster --force"
    ["ls_owner"]="$quads --ls-owner"
    ["ls_ticket"]="$quads --ls-ticket"
    ["ls_hosts"]="$quads --ls-hosts"
    ["ls_clouds"]="$quads --ls-clouds"
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
    ["sync_state"]="$quads --sync"
    ["check_move_1"]="$quads --move-hosts --dry-run --date \"2016-01-02 09:00\""
    ["check_move_2"]="$quads --move-hosts --dry-run --date \"2016-01-12 09:00\""
    )

echo ====== Initializing sample data in :  $TMPDIR

for test in $tests ; do
  action="${quads_tests[$test]}"
  echo =====================================
  echo running test \"$test\": $action
  eval $action
  retvalue=$?
  if [ $retvalue -ne 0 ]; then
      echo "Failed test: $test"
      exit $retvalue
  fi
  echo ------ current data ------
  cat $DATA
done
rm -rf $TMPDIR


