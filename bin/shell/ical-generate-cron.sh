#!/bin/sh

/root/ops-tools/lab-scheduler/ical-generate.sh $(date -d "today - 90 days" '+%Y-%m-%d') $(date -d "today + 90 days" '+%Y-%m-%d') > /srv/cal/calendars/schedule.ics && /bin/cp /srv/cal/calendars/schedule.ics /var/www/html/ical/schedule.ics
