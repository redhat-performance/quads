#!/bin/sh
#
# generate the web usage visualization for the current
# and subsequent month.  Do this daily in case the allocations
# have changed due to priority changes.

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

months_out=2
declare -A month=()
declare -A year=()
declare -A days=()

for i in $(seq 0 $months_out) ; do
    month[$i]="$(date -d "now + $i months" +%m)"
    year[$i]="$(date -d "now + $i months"  +%Y)"
    days[$i]="$(date -d "${month[$i]}/01/${year[$i]} + 1 month - 1day" +%d)"
done

source $(dirname $0)/load-config.sh
quads=${quads["install_dir"]}/bin/quads.py
bindir=${quads["install_dir"]}/bin
visual_web_dir=${quads["visual_web_dir"]}
visual_tmp_file=$(mktemp /tmp/quads-visual-tmpXXXX)

lockfile=$data_dir/.simple_table_web

if [ -f $lockfile ]; then
    if [ -d /proc/$(cat $lockfile) ]; then
        exit 0
    else
        echo $$ > $lockfile
    fi
else
    echo $$ > $lockfile
fi


[ ! -d $visual_web_dir ] && mkdir -p $visual_web_dir

for i in $(seq 0 $months_out) ; do
    $bindir/simple-table-generator.sh ${year[$i]}-${month[$i]} ${days[$i]} > $visual_tmp_file
    cp $visual_tmp_file $visual_web_dir/${year[$i]}-${month[$i]}.html
done
rm -f $visual_tmp_file

rm -f $visual_web_dir/current.html $visual_web_dir/next.html
ln -sf $visual_web_dir/${year[0]}-${month[0]}.html $visual_web_dir/current.html
ln -sf $visual_web_dir/${year[1]}-${month[1]}.html $visual_web_dir/next.html

cd $visual_web_dir
for f in $(ls *.html | sort |  egrep -v 'current|next|index') ; do
   echo "<a href=$f>$(echo $f | sed 's/.html//')</a>"
   echo "<br>"
done > index.html

