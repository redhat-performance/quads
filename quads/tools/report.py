import calendar
import logging
import sys

from quads.model import Schedule, Host
from datetime import datetime, date, timedelta

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
    next_sunday = now + timedelta(days=(6 - now.weekday()))

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
    if schedules:
        average_build = total / len(schedules)
        logger.info(f"Average build delta: {average_build}")

    hosts_summary = {}
    for host in hosts:
        host_type = host.name.split(".")[0].split("-")[-1]
        if not hosts_summary.get(host_type):
            hosts_summary[host_type] = []
        hosts_summary[host_type].append(host)

    headers = ["Server Type", "Total", "Free", "Scheduled", "2 weeks", "4 weeks"]
    logger.info(
        f"{headers[0]:>12}| "
        f"{headers[1]:>5}| "
        f"{headers[2]:>5}| "
        f"{headers[3]:>9}| "
        f"{headers[4]:>7}| "
        f"{headers[5]:>7}"
    )
    for host_type, _hosts in hosts_summary.items():
        scheduled_count = 0
        two_weeks_availability_count = 0
        four_weeks_availability_count = 0
        for host in _hosts:
            schedule = Schedule.current_schedule(host=host)
            if schedule:
                scheduled_count += 1

            two_weeks_availability = Schedule.is_host_available(
                host=host.name,
                start=next_sunday,
                end=next_sunday + timedelta(weeks=2)
            )
            if two_weeks_availability:
                two_weeks_availability_count += 1

            four_weeks_availability = Schedule.is_host_available(
                host=host.name,
                start=next_sunday,
                end=next_sunday + timedelta(weeks=4)
            )
            if four_weeks_availability:
                four_weeks_availability_count += 1

        free = len(_hosts) - scheduled_count
        schedule_percent = scheduled_count * 100 // len(_hosts)
        logger.info(
            f"{host_type:<12}| "
            f"{len(_hosts):>5}| "
            f"{free:>5}| "
            f"{schedule_percent:>8}%| "
            f"{two_weeks_availability_count:>7}| "
            f"{four_weeks_availability_count:>7}"
        )


if __name__ == "__main__":
    report(logger)
