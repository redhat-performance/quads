#!/usr/bin/bash
# This will create a QUADS sandbox locally with dummy data
# This is useful for testing purposes or when introducing
# development changes.  Requires git.
#
# USAGE: sh testing/quads-sandbox.sh

sandbox_dir=$(mktemp -d /tmp/quadsXXXX)

function init_sandbox() {
    quads_cmd="python $sandbox_dir/quads/bin/quads.py"
    cd $sandbox_dir
    git clone https://github.com/redhat-performance/quads
    cd quads
    echo "Editing QUADS configuration [$sandbox_dir/quads/conf/quads.yml]"
    sed -i -e "s@install_dir: /opt/quads@install_dir: $sandbox_dir/quads@g" $sandbox_dir/quads/conf/quads.yml
    sed -i -e "s@data_dir: /opt/quads/data@data_dir: $sandbox_dir/quads/data@g" $sandbox_dir/quads/conf/quads.yml
    sed -i -e "s@log: /opt/quads/log/quads.log@log: $sandbox_dir/quads/quads.log@g" $sandbox_dir/quads/conf/quads.yml
    echo "Creating QUADS data structure [$sandbox_dir/quads/data]"
    if ! [ -d $sandbox_dir/quads/data ]; then
        mkdir -p $sandbox_dir/quads/data
    fi
    echo "Running quads.py --init"
    $quads_cmd --init
    echo "Defining example environments [cloud01, cloud02]"
    $quads_cmd --define-cloud cloud01 --description "spare pool"
    $quads_cmd --define-cloud cloud02 --description "quads test cloud"
    echo "Defining example hosts [host01, host02, host03, host04]"
    $quads_cmd --define-host host01.example.com --default-cloud cloud01 --host-type vendor
    $quads_cmd --define-host host02.example.com --default-cloud cloud01 --host-type vendor
    $quads_cmd --define-host host03.example.com --default-cloud cloud01 --host-type vendor
    $quads_cmd --define-host host04.example.com --default-cloud cloud01 --host-type vendor
    echo "Syncing QUADS state"
    $quads_cmd --sync
    echo "Defining QUADS schedules [0, 1, 2, 3]"
    $quads_cmd --host host01.example.com --add-schedule --schedule-cloud cloud02 --schedule-start "2017-01-01 05:00" --schedule-end "2017-12-31 05:00"
    $quads_cmd --host host02.example.com --add-schedule --schedule-cloud cloud02 --schedule-start "2017-01-01 05:00" --schedule-end "2017-12-31 05:00"
    $quads_cmd --host host03.example.com --add-schedule --schedule-cloud cloud02 --schedule-start "2017-01-01 05:00" --schedule-end "2017-12-31 05:00"
    $quads_cmd --host host04.example.com --add-schedule --schedule-cloud cloud02 --schedule-start "2017-01-01 05:00" --schedule-end "2017-12-31 05:00"
    echo "Sandbox Setup!"
    echo "--------------"
    echo " You can now try commands like bin/quads.py --move-hosts --dry-run to see the result"
    cd $sandbox_dir/quads
    echo ""
    echo " QUADS sandbox location: $sandbox_dir/quads"
    echo ""
    echo "https://github.com/redhat-performance/quads#quads-usage-documentation"
    echo ""
}

init_sandbox
