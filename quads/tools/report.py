import logging
import sys

from quads.model import Schedule, Host

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logging.basicConfig(level=logging.INFO, format="%(message)s")


def report(_logger):
    _logger.info("Quads reports:")
    schedules = Schedule.objects(build_delta__ne=None)
    total = None
    for schedule in schedules:
        total = + schedule.build_delta
    average_build = total / len(schedules)
    logger.info(f"Average build delta: {average_build}")

    hosts = Host.objects()
    for host in hosts:
        schedules = Schedule.objects(host=host)


if __name__ == "__main__":
    report(logger)
