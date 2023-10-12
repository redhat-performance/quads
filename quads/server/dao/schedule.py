from datetime import datetime
from typing import List, Type
from sqlalchemy import and_

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao, EntryNotFound, InvalidArgument, SQLError
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.models import db, Host, Schedule, Cloud, Assignment


class ScheduleDao(BaseDao):
    @classmethod
    def create_schedule(
        cls, start: datetime, end: datetime, assignment: Assignment, host: Host
    ) -> Schedule:
        _schedule_obj = Schedule(start=start, end=end, assignment=assignment, host=host)
        db.session.add(_schedule_obj)
        cls.safe_commit()
        return _schedule_obj

    @classmethod
    def update_schedule(cls, sched_id: int, **kwargs) -> Schedule:
        """
        Updates a host in the database.

        :param sched_id: str: Identify the schedule to be updated to
        :param hostname: str: Identify the host to be updated to
        :param start: datetime: Pass a string with the schedule start date
        :param end: datetime: Pass a string with the schedule end date
        :param build_start: datetime: Pass a string with the schedule start build date
        :param build_end: datetime: Pass a string with the schedule end build date

        :return: The updated schedule
        """
        schedule = cls.get_schedule(sched_id)
        if not schedule:
            raise EntryNotFound

        for key, value in kwargs.items():
            if key == "hostname":
                host = HostDao.get_host(value)
                if not host:
                    raise EntryNotFound
                setattr(schedule, key, host)
                continue

            if hasattr(schedule, key):
                setattr(schedule, key, value)
            else:
                raise InvalidArgument

        result = cls.safe_commit()

        if not result:
            raise SQLError("Failed to update schedule")

        return schedule

    @classmethod
    def remove_schedule(cls, schedule_id: int) -> None:
        _schedule_obj = cls.get_schedule(schedule_id)
        if not _schedule_obj:
            raise EntryNotFound
        db.session.delete(_schedule_obj)
        cls.safe_commit()
        return

    @staticmethod
    def get_schedules() -> List[Schedule]:
        schedules = db.session.query(Schedule).all()
        return schedules

    @staticmethod
    def get_schedule(schedule_id: int) -> Schedule:
        schedule = db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
        return schedule

    @staticmethod
    def get_future_schedules(host: Host = None, cloud: Cloud = None) -> List[Schedule]:
        now = datetime.now()
        query = db.session.query(Schedule).filter(Schedule.end >= now)
        if host:
            query = query.filter(Schedule.host == host)
        if cloud:
            assignments = AssignmentDao.get_all_cloud_assignments(cloud)
            # TODO: check or_ construction

            query = query.filter(Schedule.assignment.in_(assignments))
        future_schedules = query.all()
        return future_schedules

    @staticmethod
    def filter_schedules(
        start: datetime = None,
        end: datetime = None,
        host: str = None,
        cloud: str = None,
    ) -> List[Type[Schedule]]:
        query = db.session.query(Schedule)
        if start:
            if isinstance(start, str):
                try:
                    start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M")
                    start = start_date
                except ValueError:
                    raise InvalidArgument(
                        "start argument must be a datetime object or a correct datetime format string"
                    )
            elif not isinstance(start, datetime):
                raise InvalidArgument("start argument must be a datetime object")
            query = query.filter(Schedule.start >= start)
        if end:
            if isinstance(end, str):
                try:
                    end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M")
                    end = end_date
                except ValueError:
                    raise InvalidArgument(
                        "end argument must be a datetime object or a correct datetime format string"
                    )
            elif not isinstance(end, datetime):
                raise InvalidArgument("end argument must be a datetime object")
            query = query.filter(Schedule.end <= end)
        if host:
            if not isinstance(host, str):
                raise InvalidArgument("host argument must be a str object")
            query = query.filter(Schedule.host.has(name=host))
        if cloud:
            if not isinstance(cloud, str):
                raise InvalidArgument("cloud argument must be a str object")
            cloud_obj = CloudDao.get_cloud(cloud)
            query = query.filter(Schedule.assignment.has(cloud_id=cloud_obj.id))
        filter_schedules = query.all()
        return filter_schedules

    @staticmethod
    def get_current_schedule(
        date: datetime = None, host: Host = None, cloud: Cloud = None
    ) -> List[Type[Schedule]]:
        query = db.session.query(Schedule)
        if not date:
            date = datetime.now()
        query = query.filter(and_(Schedule.start <= date, Schedule.end >= date))

        if host:
            query = query.filter(Schedule.host == host)
        # TODO: check assignment cloud schedule relationship
        if cloud:
            result = query.all()
            return [
                schedule for schedule in result if schedule.assignment.cloud == cloud
            ]
        current_schedule = query.all()
        return current_schedule

    @staticmethod
    def is_host_available(hostname, start, end, exclude=None) -> bool:
        _host = HostDao.get_host(hostname)

        if not _host:
            return False
        if _host.broken or _host.retired:
            return False
        query = db.session.query(Schedule)
        query = query.filter(Schedule.host == _host)
        if exclude:
            query = query.filter(Schedule.id != exclude)
        results = query.all()
        for result in results:
            if result.start <= start < result.end:
                return False
            if result.start < end <= result.end:
                return False
            if start < result.start and end > result.end:
                return False

        return True
