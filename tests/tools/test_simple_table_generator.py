import asyncio
from types import SimpleNamespace

from quads.tools.simple_table_generator import HostGenerate

NAIVE_SCHEDULE = {
    "assignment_id": 10,
    "start": "2026-06-01T00:00:00.000000",
    "end": "2026-06-30T23:59:59.999999",
    "description": "test workload",
    "owner": "tester",
    "ticket": "1000",
    "cloud": "cloud02",
}

RFC1123_SCHEDULE = {
    "assignment_id": 10,
    "start": "Mon, 01 Jun 2026 00:00:00 GMT",
    "end": "Tue, 30 Jun 2026 23:59:59 GMT",
    "description": "test workload",
    "owner": "tester",
    "ticket": "1000",
    "cloud": "cloud02",
}


def _allocated_days(schedule):
    generator = HostGenerate()
    generator.total_current_schedules = {"host1.example.com": [schedule]}
    host = SimpleNamespace(name="host1.example.com")
    return asyncio.run(generator.process_hosts(host, 30, 6, 2026))


def test_process_hosts_parses_naive_timestamp():
    days, allocated_count = _allocated_days(NAIVE_SCHEDULE)
    assert allocated_count == 30
    assert all(day["cloud"] == "cloud02" for day in days)


def test_process_hosts_parses_rfc1123_timestamp():
    days, allocated_count = _allocated_days(RFC1123_SCHEDULE)
    assert allocated_count == 30
    assert all(day["cloud"] == "cloud02" for day in days)


def test_process_hosts_no_schedule_defaults_to_spare_pool():
    generator = HostGenerate()
    generator.total_current_schedules = {"host1.example.com": []}
    host = SimpleNamespace(name="host1.example.com")
    days, allocated_count = asyncio.run(generator.process_hosts(host, 30, 6, 2026))
    assert allocated_count == 0
    assert all(day["cloud"] == "cloud01" for day in days)
