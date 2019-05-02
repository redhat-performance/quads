#!/usr/bin/python3

import argparse
import os
import csv
from datetime import datetime
from jinja2 import Template
from quads.config import conf, TEMPLATES_PATH
from quads.model import Schedule, Host


def generator(_host_file, _days, _month, _year, _gentime):
    if _host_file:
        with open(_host_file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    else:
        data = Host.objects()

    lines = []
    __days = []
    for i, host in enumerate(data):
        line = {"hostname": host.name}
        __days = []
        for j in range(1, _days + 1):
            cell_date = "%s-%.2d-%.2d 01:00" % (_year, _month, j)
            cell_time = datetime.strptime(cell_date, '%Y-%m-%d %H:%M')
            schedule = Schedule.current_schedule(host=host, date=cell_time).first()
            if schedule:
                chosen_color = schedule.cloud.name[5:]
            else:
                chosen_color = "01"
            _day = {
                "day": j,
                "chosen_color": chosen_color,
                "color": conf["visual_colors"]["cloud%s" % chosen_color],
                "cell_date": cell_date,
                "cell_time": cell_time
            }

            if schedule:
                _day["display_description"] = schedule.cloud.description
                _day["display_owner"] = schedule.cloud.owner
                _day["display_ticket"] = schedule.cloud.ticket
            __days.append(_day)

        line["days"] = __days
        lines.append(line)

    with open(os.path.join(TEMPLATES_PATH, "simple_table")) as _file:
        template = Template(_file.read())
    content = template.render(
        gentime=_gentime,
        _days=_days,
        lines=lines,
    )

    return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a simple HTML table with color depicting resource usage for the month')
    requiredArgs = parser.add_argument_group('Required Arguments')
    requiredArgs.add_argument('-d', '--days', dest='days', type=int, required=True, default=None,
                              help='number of days to generate')
    requiredArgs.add_argument('-m', '--month', dest='month', type=str, required=True, default=None,
                              help='Month to generate')
    requiredArgs.add_argument('-y', '--year', dest='year', type=str, required=True, default=None,
                              help='Year to generate')
    requiredArgs.add_argument('--host-file', dest='host_file', type=str, required=False, default=None,
                              help='file with list of hosts')
    parser.add_argument('--gentime', '-g', dest='gentime', type=str, required=False, default=None,
                        help='generate timestamp when created')

    args = parser.parse_args()
    host_file = args.host_file
    days = args.days
    month = args.month
    year = args.year
    gentime = args.gentime

    generator(host_file, days, month, year, gentime)
