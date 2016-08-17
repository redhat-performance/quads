#!/bin/sh
# generate markdown for an auto-generated wiki assignments page

function print_header() {
    cat <<EOF

|  SystemHostname |  OutOfBand  |  DateStartAssignment  |  DateEndAssignment  |  TotalDuration  |  DefaultEnv   | TicketNumberRT |
|-----------------|:-----------:|:---------------------:|:-------------------:|:---------------:|:--------------|:--------------:|
EOF
}

function print_summary() {
   echo "| **NAME** | **SUMMARY** |"
   echo "|----------|-------------|"
   /root/schedule.py --summary | while read line ; do
      name=$(echo $line | awk -F: '{ print $1 }')
      desc=$(echo $line | awk -F: '{ print $2 }')
      echo "| [$name](#${name}) | $desc |"
  done
  echo ""
  echo "[Unassigned Hosts](#unassigned)"
}

function print_unassigned() {
    echo ""
    echo '### <a name="unassigned"></a>Unassigned systems ###'
    echo ""
    cat <<EOF
|  SystemHostname |  OutOfBand  |
|-----------------|:-----------:|
EOF

TMPHAMMERFILE=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --per-page 10000 | grep mgmt | egrep -v 'cyclades|s4810|z9000|5548|foreman' | awk '{ print $3 }' 1>$TMPHAMMERFILE 2>&1
for h in $(cat $TMPHAMMERFILE) ; do
    nodename=$(echo $h | sed 's/mgmt-//')
    u=$(echo $h | awk -F- '{ print $3 }' | sed 's/^h//')
    short_host=$(echo $nodename | awk -F. '{ print $1 }')
    if [ "$(~/schedule.py --host $nodename)" == "None" ]; then
        echo "| $short_host | <a href=http://$h/ target=_blank>console</a> |"
    fi
done
rm -f $TMPHAMMERFILE
}

function add_row() {
    short_host=$(echo $1 | awk -F. '{ print $1 }')
    sched=$(/root/schedule.py --ls-schedule --host $1 | grep "^Current schedule:" | awk -F: '{ print $2 }')
    if [ "$sched" = "" ]; then
        defenv=""
        datestart="∞"
        dateend="∞"
        totaltime="∞"
    else
        defenv=$(/root/schedule.py --ls-schedule --host $1 | egrep "^Default cloud:" | awk -F: '{ print $2 }')
        datestart=$(/root/schedule.py --ls-schedule --host $1 | egrep "^[ ][ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $1 }' | awk -F= '{ print $2 }')
        dateend=$(/root/schedule.py --ls-schedule --host $1 | egrep "^[ ][ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $2 }' | awk -F= '{ print $2 }')
        datestartsec=$(date -d "$datestart" +%s)
        dateendsec=$(date -d "$dateend" +%s)
        totalsec=$(expr $dateendsec - $datestartsec)
        totaldays="$(expr $totalsec / 86400)"
        totalhours=$(date -d "1970-01-01 + $totalsec seconds" "+%H")
        totalminutes=$(date -d "1970-01-01 + $totalsec seconds" "+%M")
        totaltime="$totaldays day(s)"
        if [ $totalhours -gt 0 ]; then 
            totaltime="$totaltime, $totalhours hour(s)"
        fi
        if [ $totalminutes -gt 0 ]; then 
            totaltime="$totaltime, $totalminutes minute(s)"
        fi
    fi


    echo "| $short_host | <a href=http://mgmt-$1/ target=_blank>console</a> | $datestart | $dateend | $totaltime | $defenv | |"
}

# assume hostnames are the format "<rackname>-h<U location>-<type>"
function find_u() {
    echo $1 | awk -F- '{ print $3 }' | sed 's/^h//'
}

echo '### **SUMMARY**'
print_summary

echo ""

echo '### **DETAILS**'
echo ""
/root/schedule.py --summary | while read line ; do
    cloudname=$(echo $line | awk -F: '{ print $1 }')
    echo '### <a name='"$cloudname"'></a>'
    echo '### **'$line'**'
    print_header
    for h in $(/root/schedule.py --cloud-only $cloudname) ; do
        add_row $h
    done
    echo ""
done

print_unassigned

