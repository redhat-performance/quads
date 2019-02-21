import calendar
import os

from datetime import datetime, timedelta
from tools.simple_table_generator import generator
from quads.config import conf


months_out = 4
now = datetime.now()
dates = [now]

for i in range(months_out):
    previous = dates[i]
    next_date = previous + timedelta(calendar.mdays[previous.month])
    dates.append(next_date)

if not os.path.exists(conf["visual_web_dir"]):
    os.makedirs(conf["visual_web_dir"])

for _date in dates:
    gen_time = "Allocation Map for %s-%s<br>(Hover cursor over squares for details on allocation)" % (
        _date.year, _date.month)
    content = generator(None, calendar.mdays[_date.month], _date.month, _date.year, gen_time)
    file_path = os.path.join(conf["visual_web_dir"], "%s-%s.html" % (_date.year, _date.month))
    with open(file_path, "w+") as _file:
        _file.write(content)
    os.chmod(file_path, 644)

_current = os.path.join(conf["visual_web_dir"], "current.html")
_next = os.path.join(conf["visual_web_dir"], "next.html")
os.remove(_current)
os.remove(_next)

current_path = os.path.join(conf["visual_web_dir"], "%s-%s.html" % (dates[0].year, dates[0].month))
os.symlink(current_path, _current)

next_path = os.path.join(conf["visual_web_dir"], "%s-%s.html" % (dates[1].year, dates[1].month))
os.symlink(next_path, _next)

files = [html for html in os.listdir(conf["visual_web_dir"]) if ".html" in html]
lines = []
for file in files:
    if file != "current.html" and file != "next.html":
        line = "<a href=%s>%s</a>\n<br>\n" % (file, file.split(".")[0])
        lines.append(line)

index_path = os.path.join(conf["visual_web_dir"], "index.html")
with open(index_path, "w+") as index:
    for line in lines:
        index.write(line)
