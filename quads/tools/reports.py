import logging
import sys

from quads.helpers import date_span, first_day_month, last_day_month, month_delta_past, date_to_object_id
from quads.model import Schedule, Host, CloudHistory, Cloud, Q
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logging.basicConfig(level=logging.INFO, format="%(message)s")


def report_available(_logger, _start, _end):
    start = _start.replace(hour=22, minute=0, second=0)
    end = _end.replace(hour=22, minute=0, second=0)
    next_sunday = start + timedelta(days=(6 - start.weekday()))

    hosts = Host.objects(retired=False, broken=False)

    _logger.info(f"QUADS report for {start.date()} to {end.date()}:")

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
        _logger.info(f"Average build delta: {average_build}")

    hosts_summary = {}
    for host in hosts:
        host_type = host.name.split(".")[0].split("-")[-1]
        if not hosts_summary.get(host_type):
            hosts_summary[host_type] = []
        hosts_summary[host_type].append(host)

    headers = ["Server Type", "Total", "Free", "Scheduled", "2 weeks", "4 weeks"]
    _logger.info(
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
        _logger.info(
            f"{host_type:<12}| "
            f"{len(_hosts):>5}| "
            f"{free:>5}| "
            f"{schedule_percent:>8}%| "
            f"{two_weeks_availability_count:>7}| "
            f"{four_weeks_availability_count:>7}"
        )


def report_scheduled(_logger, months, year):
    headers = ["Month", "Scheduled", "Systems", "% Utilized"]
    _logger.info(
        f"{headers[0]:<8}| "
        f"{headers[1]:>8}| "
        f"{headers[2]:>8}| "
        f"{headers[3]:>11}| "
    )

    now = datetime.now()
    now = now.replace(year=year, hour=22, minute=0, second=0)
    if months:
        for month in range(months):
            process_scheduled(_logger, month, now)
    else:
        process_scheduled(_logger, months, now)


def process_scheduled(_logger, month, now):
    _date = now
    if month > 0:
        _date = month_delta_past(now, month)
    start = first_day_month(_date)
    start_id = date_to_object_id(start)
    end = last_day_month(_date)
    end_id = date_to_object_id(end)
    scheduled = CloudHistory.objects(
        __raw__={
            "_id": {
                "$lt": end_id,
                "$gt": start_id,
            },
        }
    ).order_by("-_id").count()
    hosts = Host.objects(
        __raw__={
            "_id": {
                "$lt": start_id,
            },
        }
    ).count()
    days = 0
    scheduled_count = 0
    utilization = 0
    for date in date_span(start, end):
        days += 1
        scheduled_count += Schedule.current_schedule(date=date).count()
    if hosts and days:
        utilization = scheduled_count * 100 // (days * hosts)
    f_month = f"{start.month:02}"
    _logger.info(
        f"{start.year}-{f_month:<3}| "
        f"{scheduled:>9}| "
        f"{hosts:>8}| "
        f"{utilization:>10}%| "
    )


def report_detailed(_logger, _start, _end):
    start = _start.replace(hour=21, minute=59, second=0)
    start_defer = start - timedelta(weeks=1)
    start_defer_id = date_to_object_id(start_defer)
    end = _end.replace(hour=22, minute=1, second=0)
    end_id = date_to_object_id(end)
    cloud_history = CloudHistory.objects(
        __raw__={
            "_id": {
                "$lt": end_id,
                "$gt": start_defer_id,
            },
        }
    ).order_by("-_id")

    headers = ["Owner", "Ticket", "Cloud", "Description", "Systems", "Scheduled", "Duration"]
    _logger.info(
        f"{headers[0]:<9}| "
        f"{headers[1]:>9}| "
        f"{headers[2]:>8}| "
        f"{headers[3]:>10}| "
        f"{headers[4]:>5}| "
        f"{headers[5]:>10}| "
        f"{headers[6]:>5}| "
    )

    for cloud in cloud_history:
        cloud_ref = Cloud.objects(name=cloud.name).first()
        schedule = Schedule.objects(
            Q(end__lt=end) & Q(start__gt=start) & Q(cloud=cloud_ref)
        ).order_by("-_id")
        if schedule:
            delta = schedule[0].end - schedule[0].start
            description = cloud.description[:len(headers[3])]
            _logger.info(
                f"{cloud.owner:<9}| "
                f"{cloud.ticket:>9}| "
                f"{cloud.name:>8}| "
                f"{description:>11}| "
                f"{schedule.count():>7}| "
                f"{str(schedule[0].start)[:10]:>9}| "
                f"{delta.days:>8}| "
            )


if __name__ == "__main__":
    _start = first_day_month(datetime.now())
    _end = last_day_month(datetime.now())
    report_available(logger, _start, _end)

    _months = datetime.now().month
    _year = datetime.now().year
    report_scheduled(logger, _months, _year)
