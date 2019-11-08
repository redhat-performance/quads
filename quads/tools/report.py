import calendar
import logging
import sys

from quads.model import Schedule, Host
from datetime import datetime, date

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logging.basicConfig(level=logging.INFO, format="%(message)s")


def report(_logger):
    _logger.info("Quads reports:")

    now = datetime.now()
    month = now.month
    days = calendar.mdays[month]
    hosts = Host.objects()

    total_allocated_month = 0
    total_hosts = len(hosts)
    for day in range(1, days + 1):
        schedules = Schedule.current_schedule(date=date(now.year, month, day)).count()
        total_allocated_month += schedules
    utilized = total_allocated_month * 100 // (total_hosts * days)
    _logger.info(f"Percentage Utilized for {now.year}-{month}: {utilized}%")

    schedules = Schedule.objects(build_delta__ne=None)
    total = 0
    for schedule in schedules:
        total = + schedule.build_delta
    average_build = total / len(schedules)
    logger.info(f"Average build delta: {average_build}")

    hosts_summary = {}
    for host in hosts:
        host_type = host.name.split(".")[0].split("-")[-1]
        if not hosts_summary.get(host_type):
            hosts_summary[host_type] = []
        hosts_summary[host_type].append(host)

    logger.info(f"Server Type | Total in fleet | Total Free | Scheduled ")

    for host_type, _hosts in hosts_summary.items():
        scheduled_count = 0
        for host in _hosts:
            schedule = Schedule.current_schedule(host=host)
            if schedule:
                scheduled_count += 1
        free = len(_hosts) - scheduled_count
        logger.info(
            f"{host_type} | {len(_hosts)} | {free} | {scheduled_count}"
        )


if __name__ == "__main__":
    report(logger)
