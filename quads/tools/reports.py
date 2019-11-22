import calendar
import logging
import sys

from quads.helpers import date_span
from quads.model import Schedule, Host
from datetime import timedelta

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logging.basicConfig(level=logging.INFO, format="%(message)s")


def report_available(_logger, _start, _end):
    start = _start.replace(hour=22, minute=0, second=0)
    end = _end.replace(hour=22, minute=0, second=0)
    next_sunday = start + timedelta(days=(6 - start.weekday()))

    hosts = Host.objects()

    _logger.info(f"Quads report for {start} to {end}:")

    days = 0
    total_allocated_month = 0
    total_hosts = len(hosts)
    for _date in date_span(start, end):
        total_allocated_month += Schedule.current_schedule(date=_date).count()
        days += 1
    utilized = total_allocated_month * 100 // (total_hosts * days)
    _logger.info(f"Percentage Utilized: {utilized}%")

    schedules = Schedule.objects(build_start__ne=None, build_end__ne=None)
    total = timedelta()
    for schedule in schedules:
        total += schedule.build_end - schedule.build_start
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
        f"{headers[0]:<12}| "
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
    report_available(logger)
