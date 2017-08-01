#!/bin/sh
# generate markdown for an auto-generated wiki assignments page

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
quads_url=${quads["quads_url"]}
rt_url=${quads["rt_url"]}
data_dir=${quads["data_dir"]}
exclude_hosts=${quads["exclude_hosts"]}
domain=${quads["domain"]}

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
   $quads --summary | while read line ; do
      name=$(echo $(echo $line | awk -F: '{ print $1 }'))
      desc=$(echo $(echo $line | awk -F: '{ print $2 }'))
      owner=$($quads --ls-owner --cloud-only $name)
      rt=$($quads --ls-ticket --cloud-only $name)
      if [ "$rt" ]; then
          link="<a href=${rt_url}?id=$rt target=_blank>$rt</a>"
      else
          link=""
      fi
      $quads --cloud-only ${name} > $tmpsummary
      echo "| [$name](#${name}) | $desc | $owner | $link | <a href=${quads_url}/cloud/${name}_instackenv.json target=_blank>$name</a> |"
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

TMPHAMMERFILE1=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
TMPHAMMERFILE2=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
TMPHAMMERFILE3=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --per-page 10000 1>$TMPHAMMERFILE1 2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
cat $TMPHAMMERFILE1 | grep mgmt | egrep -v "$exclude_hosts" | awk '{ print $3 }' 1>$TMPHAMMERFILE2 2>&1
hammer host list --search params.broken_state=true 1>$TMPHAMMERFILE1 2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
cat $TMPHAMMERFILE1 | grep $domain | awk '{ print $3 }' 1>$TMPHAMMERFILE3 2>&1
for h in $(cat $TMPHAMMERFILE2) ; do
    nodename=$(echo $h | sed 's/mgmt-//')
    if grep -q $nodename $TMPHAMMERFILE3 ; then
        :
    else
        u=$(echo $h | awk -F- '{ print $3 }' | sed 's/^h//')
        short_host=$(echo $nodename | awk -F. '{ print $1 }')
        if [ "$($quads --host $nodename)" == "None" ]; then
           echo "| $short_host | <a href=http://$h/ target=_blank>console</a> |"
        fi
    fi
done
rm -f $TMPHAMMERFILE1 $TMPHAMMERFILE2 $TMPHAMMERFILE3
}

function print_faulty() {
    echo ""
    echo '### <a name="faulty"></a>Faulty systems ###'
    echo ""
    cat <<EOF
| **SystemHostname** | **OutOfBand** |
|--------------------|---------------|
EOF

TMPHAMMERFILE1=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
TMPHAMMERFILE2=$(mktemp /tmp/hammer_host_list_XXXXXXXX)
hammer host list --search params.broken_state=true 1>$TMPHAMMERFILE1 2>&1
if [ $? -gt 0 ]; then
    exit 1
fi
cat $TMPHAMMERFILE1 | grep $domain | awk '{ print $3 }' 1>$TMPHAMMERFILE2 2>&1
for h in $(cat $TMPHAMMERFILE2) ; do
    nodename=$(echo $h | sed 's/mgmt-//')
    u=$(echo $h | awk -F- '{ print $3 }' | sed 's/^h//')
    short_host=$(echo $nodename | awk -F. '{ print $1 }')
    echo "| $short_host | <a href=http://mgmt-$h/ target=_blank>console</a> |"
done
rm -f $TMPHAMMERFILE1 $TMPHAMMERFILE2
}

function add_row() {
    short_host=$(echo $1 | awk -F. '{ print $1 }')
    sched=$($quads --ls-schedule --host $1 | grep "^Current schedule:" | awk -F: '{ print $2 }')
    defenv=$($quads --ls-schedule --host $1 | egrep "^Default cloud:" | awk -F: '{ print $2 }')
    if [ "$sched" = "" ]; then
        datestart="∞"
        dateend="∞"
        totaltime="∞"
        totaltimeleft="∞"
    else
        datestart=$($quads --ls-schedule --host $1 | egrep "^[ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $1 }' | awk -F= '{ print $2 }')
        dateend=$($quads --ls-schedule --host $1 | egrep "^[ ]*$sched\|" | awk -F\| '{ print $2 }' | awk -F, '{ print $2 }' | awk -F= '{ print $2 }')
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
        if [ $totalhoursleft -gt 0 ]; then 
            totaltimeleft="$totaltimeleft, $totalhoursleft hour(s)"
        fi
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
$quads --summary | while read line ; do
    cloudname=$(echo $line | awk -F: '{ print $1 }')
    cloudowner=$($quads --ls-owner --cloud-only $cloudname)
    echo '### <a name='"$cloudname"'></a>'
    echo '### **'$line -- $cloudowner'**'
    print_header
    for h in $($quads --cloud-only $cloudname) ; do
        add_row $h
    done
    echo ""
done

print_unmanaged
print_faulty

