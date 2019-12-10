#!/usr/bin/env python3
# generate simple report from quads-cli data
# TODO:  reference reports.py / QUADS data here instead of temp-report-data.txt
# TODO:  fix iteration issues, only one line of systems is reporting
# TODO:  Ideally this should look like this:
#        http://us.funcamp.net:9999/et.html
#        https://funcamp.net/w/et.html
### WIP REMOVE ME ###
header_row = """
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
.tg .tg-edkc{font-size:28px;vertical-align:top}
.tg .tg-24i8{font-size:24px;vertical-align:top}
</style>
<table class="tg">
<html>
<table>
<tr>
<th class="tg-edkc">Server Type</th>
<th class="tg-edkc">Total</th>
<th class="tg-edkc">Free</th>
<th class="tg-edkc">Scheduled</th>
<th class="tg-edkc">2 Weeks Free</th>
<th class="tg-edkc">4 Weeks Free</th>
</tr>
"""

#### FIX ME
#### DO not use temp-report-data.txt
#### Use QUADS or reports library here

def genoverview():
    with open("temp-report-data.txt") as f:
        lines = f.readlines()
        for line in lines[3:-1]:
            Type = line.split("|")
            servertype = Type[0]
            total = Type[1]
            free = Type[2]
            sched = Type[3]
            twoweek = Type[4]
            fourweek = Type[5]
            tabledata = ("<tr><td class='tg-24i8'>" +servertype + "</td>\n"
                     + "<td class='tg-24i8'>" +total + "</td>\n"
                     + "<td class='tg-24i8'>" +free + "</td>\n"
                     + "<td class='tg-24i8'>" +sched + "</td>\n"
                     + "<td class='tg-24i8'>" +twoweek + "</td>\n"
                     + "<td class='tg-24i8'>" +fourweek + "</td></tr>\n"
                     )
        rawtable = (header_row + tabledata)
        fulltable = (rawtable + "</table></html")

    print(fulltable)


genoverview()
