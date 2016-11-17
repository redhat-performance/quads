#!/bin/sh

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

bindir=${quads["install_dir"]}/bin
phpical_dir=${quads["phpical_dir"]}
ical_web_location=${quads["ical_web_location"]}


$bindir/ical-generate.sh $(date -d "today - 90 days" '+%Y-%m-%d') $(date -d "today + 90 days" '+%Y-%m-%d') > $phpical_dir/calendars/schedule.ics && /bin/cp $phpical_dir/calendars/schedule.ics $ical_web_location
