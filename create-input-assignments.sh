#!/bin/sh
# generate markdown for an auto-generated wiki assignments page

function print_header() {
    cat <<EOF

|  SystemHostname |  OutOfBand  |  DateStartAssignment  |  DateEndAssignment  | TotalDuration  | TimeRemaining |  Graph  |
|-----------------|:-----------:|:---------------------:|:-------------------:|:--------------:|:-------------:|:--------|
EOF
}

function print_summary() {
   tmpsummary=$(mktemp /tmp/cloudSummaryXXXXXX)
   echo "| **NAME** | **SUMMARY** | **OWNER** | **REQUEST** | **INSTACKENV** |"
   echo "|----------|-------------|-----------|--------------------|----------------|"
   /root/schedule.py --summary | while read line ; do
      name=$(echo $(echo $line | awk -F: '{ print $1 }'))
      desc=$(echo $(echo $line | awk -F: '{ print $2 }'))
      owner=$(/root/schedule.py --ls-owner --cloud-only $name)
      rt=$(/root/schedule.py --ls-ticket --cloud-only $name)
      if [ "$rt" ]; then
          link="<a href=https://engineering.example.com/rt/Ticket/Display.html?id=$rt target=_blank>$rt</a>"
      else
          link=""
      fi
      ~/schedule.py --cloud-only ${name} > $tmpsummary
      if [ -f /etc/lab/undercloud/$name ]; then
          uc=$(cat /etc/lab/undercloud/$name)
      else
          uc=$(head -1 $tmpsummary)
      fi
      echo "| [$name](#${name}) | $desc | $owner | $link | <a href=http://quads.scalelab.example.com/cloud/${name}_${uc}_instackenv.json target=_blank>$name</a> |"
      rm -f $tmpsummary
  done
  echo ""
  echo "[Unmanaged Hosts](#unmanaged)"
  echo ""
  echo "[Faulty  Hosts](#faulty)"
}

function print_unmanaged() {
    echo ""
    echo '### <a name="unmanaged"></a>Unmanaged systems ###'
    echo ""
    cat <<EOF
| **SystemHostname** | **OutOfBand** |
|--------------------|---------------|
EOF

TMPHAMMERFILE=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
TMPHAMMERFILE2=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --per-page 10000 | grep mgmt | egrep -v 'cyclades|s4810|z9000|5548|foreman|c08-h30-r630|c08-h05-r930|b08-|e05-h25|zfs01' | awk '{ print $3 }' 1>$TMPHAMMERFILE 2>&1
hammer host list --search params.broken_state=true | grep example.com | awk '{ print $3 }' 1>$TMPHAMMERFILE2 2>&1
for h in $(cat $TMPHAMMERFILE) ; do
    nodename=$(echo $h | sed 's/mgmt-//')
    if grep -q $nodename $TMPHAMMERFILE2 ; then
        :
    else
        u=$(echo $h | awk -F- '{ print $3 }' | sed 's/^h//')
        short_host=$(echo $nodename | awk -F. '{ print $1 }')
        if [ "$(~/schedule.py --host $nodename)" == "None" ]; then
           echo "| $short_host | <a href=http://$h/ target=_blank>console</a> |"
        fi
    fi
done
rm -f $TMPHAMMERFILE $TMPHAMMERFILE2
}

function print_faulty() {
    echo ""
    echo '### <a name="faulty"></a>Faulty systems ###'
    echo ""
    cat <<EOF
| **SystemHostname** | **OutOfBand** |
|--------------------|---------------|
EOF

TMPHAMMERFILE=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --search params.broken_state=true | grep example.com | awk '{ print $3 }' 1>$TMPHAMMERFILE 2>&1
for h in $(cat $TMPHAMMERFILE) ; do
    nodename=$(echo $h | sed 's/mgmt-//')
    u=$(echo $h | awk -F- '{ print $3 }' | sed 's/^h//')
    short_host=$(echo $nodename | awk -F. '{ print $1 }')
    echo "| $short_host | <a href=http://mgmt-$h/ target=_blank>console</a> |"
done
rm -f $TMPHAMMERFILE
}

function add_row() {
    short_host=$(echo $1 | awk -F. '{ print $1 }')
    sched=$(/root/schedule.py --ls-schedule --host $1 | grep "^Current schedule:" | awk -F: '{ print $2 }')
    defenv=$(/root/schedule.py --ls-schedule --host $1 | egrep "^Default cloud:" | awk -F: '{ print $2 }')
    if [ "$sched" = "" ]; then
        datestart="∞"
        dateend="∞"
        totaltime="∞"
        totaltimeleft="∞"
    else
        datestart=$(/root/schedule.py --ls-schedule --host $1 | egrep "^[ ][ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $1 }' | awk -F= '{ print $2 }')
        dateend=$(/root/schedule.py --ls-schedule --host $1 | egrep "^[ ][ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $2 }' | awk -F= '{ print $2 }')
        datenowsec=$(date +%s)
        datestartsec=$(date -d "$datestart" +%s)
        dateendsec=$(date -d "$dateend" +%s)
        totalsec=$(expr $dateendsec - $datestartsec)
        totalsecleft=$(expr $dateendsec - $datenowsec)
        totaldays="$(expr $totalsec / 86400)"
        totaldaysleft="$(expr $totalsecleft / 86400)"
        totalhours=$(date -d "1970-01-01 + $totalsec seconds" "+%H")
        totalhoursleft=$(date -d "1970-01-01 + $totalsecleft seconds" "+%H")
        totalminutes=$(date -d "1970-01-01 + $totalsec seconds" "+%M")
        totalminutesleft=$(date -d "1970-01-01 + $totalsecleft seconds" "+%M")
        totaltime="$totaldays day(s)"
        totaltimeleft="$totaldaysleft day(s)"
        if [ $totalhours -gt 0 ]; then 
            totaltime="$totaltime, $totalhours hour(s)"
        fi
#        if [ $totalminutes -gt 0 ]; then 
#            totaltime="$totaltime, $totalminutes minute(s)"
#        fi
        if [ $totalhoursleft -gt 0 ]; then 
            totaltimeleft="$totaltimeleft, $totalhoursleft hour(s)"
        fi
#        if [ $totalminutesleft -gt 0 ]; then 
#            totaltime="$totaltimeleft, $totalminutesleft minute(s)"
#        fi
    fi


    echo "| $short_host | <a href=http://mgmt-$1/ target=_blank>console</a> | $datestart | $dateend | $totaltime | $totaltimeleft | |"
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
    cloudowner=$(/root/schedule.py --ls-owner --cloud-only $cloudname)
    echo '### <a name='"$cloudname"'></a>'
    echo '### **'$line -- $cloudowner'**'
    print_header
    for h in $(/root/schedule.py --cloud-only $cloudname) ; do
        add_row $h
    done
    echo ""
done

print_unmanaged
print_faulty

