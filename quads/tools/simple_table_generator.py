#!/usr/bin/env python3


import argparse
import os
import csv
from datetime import datetime
from jinja2 import Template
from quads.config import conf, API_URL, TEMPLATES_PATH
from quads.model import Cloud, Schedule, Host
from quads.quads import Api


def print_simple_table(data, data_colors, _days, _month, _year, _gentime, color_array):
    lines = []
    __days = []
    for i, host in enumerate(data):
        line = {"hostname": host.name}
        __days = []
        for j in range(0, _days):
            chosen_color = data_colors[i][j-1]
            cell_date = "%s-%.2d-%.2d 00:00" % (_year, _month, int(j+1))
            _day = {
                "day": j + 1,
                "chosen_color": chosen_color,
                "color": color_array[int(chosen_color) - 1],
                "cell_date": cell_date,
                "cell_time": datetime.strptime(cell_date, '%Y-%m-%d %H:%M')
            }

            cloud_history = Schedule.objects(host=host)
            for schedule in cloud_history:
                if schedule.start <= _day["cell_time"]:
                    _cloud_obj = Cloud.objects(cloud=schedule.cloud)
                    _day["display_description"] = _cloud_obj.description
                    _day["display_owner"] = _cloud_obj.owner
                    _day["display_ticket"] = _cloud_obj.ticket
                break
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


def generator(_host_file, _days, _month, _year, _gentime):
    quads = Api(API_URL)

    if _host_file:
        with open(_host_file, 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)
    else:
        your_list = Host.objects()
    your_list_colors = []
    for _host in your_list:
        one_host = []
        for d in range(0, _days - 1):
            day = d + 1
            if day < 10:
                day_string = "0" + str(day)
            else:
                day_string = str(day)
            current = quads.get_current_schedule(
                host=_host.name, date="{}-{}-{} 00:00".format(_year, _month, day_string)
            )
            if current and "result" not in current:
                _cloud_obj = Cloud.objects(id=current[0]["cloud"]["$oid"]).first()
                one_host.append(_cloud_obj.name.lstrip("cloud"))
            else:
                one_host.append("01")
        your_list_colors.append(one_host)

    return print_simple_table(your_list, your_list_colors, _days, _month, _year, _gentime, conf["visual_colors"])


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
