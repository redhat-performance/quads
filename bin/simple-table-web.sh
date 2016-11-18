#!/bin/sh
#
# generate the web usage visualization for the current
# and subsequent month.  Do this daily in case the allocations
# have changed due to priority changes.

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh
quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
visual_web_dir=${quads["visual_web_dir"]}

currentmonth=$(date +"%m")
currentyear=$(date +"%Y")
currentmonthdays=$(date -d "$currentmonth/01/$currentyear + 1 month - 1 day" +%d)

nextmonth=$(date -d 'next month' +"%m")
nextyear=$(date -d 'next month' +"%Y")
nextmonthdays=$(date -d "$nextmonth/01/$nextyear + 1 month - 1 day" +%d)

[ ! -d $visual_web_dir ] && mkdir -p $visual_web_dir

$bindir/simple-table-generator.sh ${currentyear}-${currentmonth} $currentmonthdays > $visual_web_dir/${currentyear}-${currentmonth}.html
$bindir/simple-table-generator.sh ${nextyear}-${nextmonth} $nextmonthdays > $visual_web_dir/${nextyear}-${nextmonth}.html

rm -f $visual_web_dir/current.html $visual_web_dir/next.html
ln -sf $visual_web_dir/${currentyear}-${currentmonth}.html $visual_web_dir/current.html
ln -sf $visual_web_dir/${nextyear}-${nextmonth}.html $visual_web_dir/next.html

cd $visual_web_dir
for f in $(ls *.html | sort |  egrep -v 'current|next|index') ; do
   echo "<a href=$f>$(echo $f | sed 's/.html//')</a>"
done > index.html

