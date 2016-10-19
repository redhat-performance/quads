#!/bin/sh

startdate=$1
enddate=$2

daterangecmd=/root/ops-tools/lab-scheduler/date-range-generate.py
schedcmd=/root/schedule.py
summaryloc=/etc/lab/summary

$schedcmd --summary > $summaryloc/$(date +%Y-%m-%d)

cat <<EOF
BEGIN:VCALENDAR
X-WR-CALNAME:Scale Lab Allocations
X-WR-CALID:1aeca593-a063-461b-9218-f45e649faab0:314654
PRODID:Zimbra-Calendar-Provider
VERSION:2.0
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:America/New_York
BEGIN:STANDARD
DTSTART:16010101T020000
TZOFFSETTO:-0500
TZOFFSETFROM:-0400
RRULE:FREQ=YEARLY;WKST=MO;INTERVAL=1;BYMONTH=11;BYDAY=1SU
TZNAME:EST
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:16010101T020000
TZOFFSETTO:-0400
TZOFFSETFROM:-0500
RRULE:FREQ=YEARLY;WKST=MO;INTERVAL=1;BYMONTH=3;BYDAY=2SU
TZNAME:EDT
END:DAYLIGHT
END:VTIMEZONE
EOF

for d in $($daterangecmd --start-date "$startdate 00:00" --end-date "$enddate 00:00" | awk '{ print $1 }'); do
    dtstart=`date -d $d +%Y%m%d`
    dtend=`date -d "$d + 1 day" +%Y%m%d`
    cat <<EOF
BEGIN:VEVENT
UID:$d@scalelab
SUMMARY:$d
EOF
    echo -n "DESCRIPTION:\\n"
    # for dates in the past, generate a cached summary once
    if [ $(date +%s -d $d) -lt $(date +%s -d $(date +%Y-%m-%d)) ]; then
        # if you already have the summary, use it
        if [ -f $summaryloc/$d ]; then
            cat $summaryloc/$d | sed 's,$,\\n,' | sed 's/^/ /g'
        # otherwise generate it.  this will speed up next runs
        else
            $schedcmd --summary --date "$d 00:00" > $summaryloc/$d
            cat $summaryloc/$d | sed 's,$,\\n,' | sed 's/^/ /g'
        fi
    # anything for today and forward is subject to change.
    else
        $schedcmd --summary --date "$d 00:00" | sed 's,$,\\n,' | sed 's/^/ /g'
    fi
    cat <<EOF
LOCATION:Scale Lab
DTSTART;VALUE=DATE:$dtstart
DTEND;VALUE=DATE:$dtend
STATUS:CONFIRMED
CLASS:PUBLIC
X-MICROSOFT-CDO-ALLDAYEVENT:TRUE
X-MICROSOFT-CDO-INTENDEDSTATUS:FREE
TRANSP:TRANSPARENT
LAST-MODIFIED:20100713T125033Z
DTSTAMP:20100713T125033Z
SEQUENCE:8
END:VEVENT
EOF
done
cat <<EOF
END:VCALENDAR
EOF

