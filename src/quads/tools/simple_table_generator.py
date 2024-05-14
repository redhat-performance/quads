#!/usr/bin/env python3

import argparse
import os
import csv
from datetime import datetime
import random

from jinja2 import Template
from quads.config import Config
from quads.quads_api import QuadsApi


def random_color():
    def rand():
        return random.randint(100, 255)

    return "#%02X%02X%02X" % (rand(), rand(), rand())


def generator(_host_file, _days, _month, _year, _gentime):
    quads = QuadsApi(Config)
    if _host_file:
        with open(_host_file, "r") as f:
            reader = csv.reader(f)
            hosts = list(reader)
    else:
        filtered_hosts = quads.filter_hosts(data={"retired": False, "broken": False})
        hosts = sorted(filtered_hosts, key=lambda x: x.name)

<<<<<<< Updated upstream
    lines = []
    __days = []
    non_allocated_count = 0
    all_samples = []
    all_samples.extend(range(129296, 129510))
    all_samples.extend(range(128000, 128252))
    samples = random.sample(all_samples, 200)
    exclude = [129401, 129484]
    emojis = [emoji for emoji in samples if emoji not in exclude]
    colors = [random_color() for _ in range(100)]
    colors[0] = "#A9A9A9"
    for i, host in enumerate(hosts):
        line = {"hostname": host.name}
        __days = []
=======
    BLOCK_SIZE = 10

    def __init__(self):
        self.total_current_schedules = {}
        self.quads_async = QuadsApiAsync(Config)
        self.colors = []
        self.emojis = []
        self.hosts = []
        self.generate_colors()

    def random_color(self):
        def rand():
            return random.randint(100, 255)

        return "#%02X%02X%02X" % (rand(), rand(), rand())

    def generate_colors(self):
        all_samples = []
        all_samples.extend(range(129296, 129510))
        all_samples.extend(range(128000, 128252))
        samples = random.sample(all_samples, 200)
        exclude = [129401, 129484]
        self.emojis = [emoji for emoji in samples if emoji not in exclude]
        self.colors = [self.random_color() for _ in range(100)]
        self.colors[0] = "#A9A9A9"

    async def fetch_schedule(self, payload):
        schedules = await self.quads_async.async_get_current_schedules(payload)
        if schedules:
            schedule = schedules[0]
            chosen_color = schedule.assignment.cloud.name[5:]
            return schedule, chosen_color
        else:
            return None, "01"

    async def order_current_schedules_by_hostname(self):
        total_current_schedules = await self.quads_async.async_get_current_schedules()
        for schedule in total_current_schedules:
            self.total_current_schedules[schedule.host.name] = schedule

    async def get_current_host_schedules(self, host_name):
        if self.total_current_schedules is None:
            await self.order_current_schedules_by_hostname()
        return self.total_current_schedules.get(host_name, None)

    async def process_hosts(self, host, _days, _month, _year):
        non_allocated_count = 0
        __days = []
        schedules = await self.get_current_host_schedules(host.name)
        schedule = schedules
        chosen_color = schedules.assignment.cloud.name[5:] if schedule else "01"
>>>>>>> Stashed changes
        for j in range(1, _days + 1):
            cell_date = "%s-%.2d-%.2d 01:00" % (_year, _month, j)
            cell_time = datetime.strptime(cell_date, "%Y-%m-%d %H:%M")
            datearg_iso = cell_time.isoformat()
            date_str = ":".join(datearg_iso.split(":")[:-1])
            payload = {"host": host.name, "date": date_str}
            schedule = None
            schedules = quads.get_current_schedules(payload)
            if schedules:
                schedule = schedules[0]
                chosen_color = schedule.assignment.cloud.name[5:]
            else:
                non_allocated_count += 1
                chosen_color = "01"
            _day = {
                "day": j,
                "chosen_color": chosen_color,
                "emoji": "&#%s;" % emojis[int(chosen_color) - 1],
                "color": colors[int(chosen_color) - 1],
                "cell_date": cell_date,
                "cell_time": cell_time,
            }

            if schedule:
                assignment = schedule.assignment
                _day["display_description"] = assignment.description
                _day["display_owner"] = assignment.owner
                _day["display_ticket"] = assignment.ticket
            __days.append(_day)

<<<<<<< Updated upstream
        line["days"] = __days
        lines.append(line)

    total_hosts = len(hosts)
    total_use = len(quads.get_current_schedules())
    utilization = 100 - (non_allocated_count * 100 // (_days * total_hosts))
    utilization_daily = total_use * 100 // total_hosts
    with open(os.path.join(Config.TEMPLATES_PATH, "simple_table_emoji")) as _file:
        template = Template(_file.read())
    content = template.render(
        gentime=_gentime,
        _days=_days,
        lines=lines,
        utilization=utilization,
        utilization_daily=utilization_daily,
        total_use=total_use,
        total_hosts=total_hosts,
    )

    return content
=======
    async def generator(self, _host_file, _days, _month, _year, _gentime):
        if _host_file:
            with open(_host_file, "r") as f:
                reader = csv.reader(f)
                hosts = list(reader)
        else:
            if not self.hosts:
                filtered_hosts = await self.quads_async.async_filter_hosts(data={"retired": False, "broken": False})
                self.hosts = sorted(filtered_hosts, key=lambda x: x.name)
            hosts = self.hosts

        await self.order_current_schedules_by_hostname()
        total_current_schedules = self.total_current_schedules
                
        lines = []
        __days = []
        non_allocated_count = 0
        host_blocks = [hosts[i:i + self.BLOCK_SIZE] for i in
                       range(0, len(hosts), self.BLOCK_SIZE)]

        for host_block in host_blocks:
            tasks = [self.process_hosts(host, _days, _month, _year) for host in host_block]
            results = await asyncio.gather(*tasks)

            for host, (days, non_allocated) in zip(host_block, results):
                lines.append({"hostname": host.name, "days": days})
                non_allocated_count += non_allocated

        total_hosts = len(hosts)
        total_use = len(total_current_schedules)
        utilization = 100 - (non_allocated_count * 100 // (_days * total_hosts))
        utilization_daily = total_use * 100 // total_hosts
        with open(os.path.join(Config.TEMPLATES_PATH, "simple_table_emoji")) as _file:
            template = Template(_file.read())
        content = template.render(
            gentime=_gentime,
            _days=_days,
            lines=lines,
            utilization=utilization,
            utilization_daily=utilization_daily,
            total_use=total_use,
            total_hosts=total_hosts,
        )

        return content
>>>>>>> Stashed changes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a simple HTML table with color depicting resource usage for the month"
    )
    requiredArgs = parser.add_argument_group("Required Arguments")
    requiredArgs.add_argument(
        "-d",
        "--days",
        dest="days",
        type=int,
        required=True,
        default=None,
        help="number of days to generate",
    )
    requiredArgs.add_argument(
        "-m",
        "--month",
        dest="month",
        type=str,
        required=True,
        default=None,
        help="Month to generate",
    )
    requiredArgs.add_argument(
        "-y",
        "--year",
        dest="year",
        type=str,
        required=True,
        default=None,
        help="Year to generate",
    )
    requiredArgs.add_argument(
        "--host-file",
        dest="host_file",
        type=str,
        required=False,
        default=None,
        help="file with list of hosts",
    )
    parser.add_argument(
        "--gentime",
        "-g",
        dest="gentime",
        type=str,
        required=False,
        default=None,
        help="generate timestamp when created",
    )

    args = parser.parse_args()
    host_file = args.host_file
    days = args.days
    month = args.month
    year = args.year
    gentime = args.gentime

    generator(host_file, days, month, year, gentime)
