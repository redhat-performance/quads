#!/usr/bin/env python3


import argparse
import os
import csv
from datetime import datetime
from jinja2 import Template
from quads.config import conf as quads_config, API_URL, TEMPLATES_PATH
from quads.quads import Api


def generator(_host_file, _days, _month, _year, _gentime):
    color_array = []

    quads = Api(API_URL)

    def get_spaced_colors(visual_colors):
        result = []
        for k in sorted(visual_colors.keys()):
            result.append(visual_colors[k].split())
        return result

    # covert palette to hex
    def get_cell_color(a, b, c):
        return "#" + \
               ('0' if len(hex(int(a))) < 4 else '') + hex(int(a))[2:] + \
               ('0' if len(hex(int(b))) < 4 else '') + hex(int(b))[2:] + \
               ('0' if len(hex(int(c))) < 4 else '') + hex(int(c))[2:]

    colors = get_spaced_colors(quads_config["visual_colors"])
    for i in colors:
        if int(i[0]) >= 0:
            color_array.append(get_cell_color(i[0], i[1], i[2]))
        else:
            color_array.append(i[1])

    def print_simple_table(data, data_colors, _days, _gentime):
        lines = []
        for item in range(len(data)):
            line = {"hostname": str(data[item][0])}
            __days = []
            for j in range(1, _days):
                chosen_color = data_colors[item][j - 1]
                cell_date = "%s-%s-%.2d 00:00" % (_year, _month, int(j))
                _day = {
                    "day": j,
                    "chosen_color": chosen_color,
                    "color": color_array[int(chosen_color) - 1],
                    "cell_date": cell_date,
                    "cell_time": datetime.strptime(cell_date, '%Y-%m-%d %H:%M')
                }

                # TODO: this
                # history = quads.get_history()
                # for cloud in sorted(history["cloud" + str(_day["chosen_color"])]):
                #     if datetime.fromtimestamp(cloud) <= _day["cell_time"]:
                #         _day["display_description"] = \
                #             history["cloud" + str(_day["chosen_color"])][cloud]["description"]
                #         _day["display_owner"] = history["cloud" + str(_day["chosen_color"])][cloud]["owner"]
                #         _day["display_ticket"] = history["cloud" + str(_day["chosen_color"])][cloud]["ticket"]
                #         break
                __days.append(_day)

            line["days"] = __days
            lines.append(line)

        with open(os.path.join(TEMPLATES_PATH, "simple_table")) as _file:
            template = Template(_file.read)
        content = template.render(
            gentime=_gentime,
            _days=_days,
            lines=lines,
        )

        return content

    if _host_file:
        with open(_host_file, 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)
    else:
        your_list = []
        for h in sorted(quads.get_hosts()):
            your_list.append([h])
    your_list_colors = []
    for h in your_list:
        one_host = []
        for d in range(0, _days):
            day = d + 1
            if day < 10:
                day_string = "0" + str(day)
            else:
                day_string = str(day)
            current = quads.get_current_schedule(host=h[0], date="{}-{}-{} 00:00".format(_year, _month, day_string))
            if current:
                one_host.append(current["cloud"].lstrip("cloud"))
        your_list_colors.append(one_host)

    return print_simple_table(your_list, your_list_colors, _days, _gentime)


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
