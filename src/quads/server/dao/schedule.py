from datetime import datetime
from typing import List, Type

from sqlalchemy import Boolean, and_

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import (
    OPERATORS,
    BaseDao,
    EntryNotFound,
    InvalidArgument,
    SQLError,
)
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.models import Assignment, Cloud, Host, Schedule, db


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
        if not schedule:  # pragma: no cover
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

        if not result:  # pragma: no cover
            raise SQLError("Failed to update schedule")

        return schedule

    @classmethod
    def remove_schedule(cls, schedule_id: int) -> None:
        _schedule_obj = cls.get_schedule(schedule_id)
        if not _schedule_obj:  # pragma: no cover
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
            query = query.join(Assignment).filter(
                Assignment.id.in_((ass.id for ass in assignments))
            )
        future_schedules = query.all()
        return future_schedules

    @staticmethod
    def filter_schedule_dict(data: dict) -> List[Schedule]:
        filter_tuples = []
        date_fields = ["start", "end", "build_start", "build_end"]
        operator = "=="
        group_by = None
        for k, value in data.items():
            fields = k.split(".")
            if len(fields) > 2:
                raise InvalidArgument(f"Too many arguments: {fields}")

            first_field = fields[0]
            field_name = fields[-1]
            if "__" in k:
                for op in OPERATORS.keys():
                    if op in field_name:
                        if first_field == field_name:
                            first_field = field_name[: field_name.index(op)]
                        field_name = field_name[: field_name.index(op)]
                        operator = OPERATORS[op]
                        break

            if value.lower() == "none":
                value = None

            if fields[0].lower() == "group_by":
                first_field = value
                group_by = value
                k = value
            field = Schedule.__mapper__.attrs.get(first_field)
            if not field:
                raise InvalidArgument(f"{k} is not a valid field.")
            try:
                if type(field.columns[0].type) == Boolean:
                    value = value.lower() in ["true", "y", 1, "yes"]
            except AttributeError:
                if first_field.lower() == "host":
                    host = HostDao.get_host(value)
                    if not host:
                        raise EntryNotFound(f"Host not found: {value}")
                    value = host
                    field_name = first_field

            if first_field in date_fields:
                try:
                    if value:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M")
                except ValueError:
                    raise InvalidArgument(
                        f"Invalid date format for {first_field}: {value}"
                    )

            if fields[0].lower() != "group_by":
                filter_tuples.append(
                    (
                        field_name,
                        operator,
                        value,
                    )
                )
        try:
            _schedules = ScheduleDao.create_query_select(
                Schedule, filters=filter_tuples, group_by=group_by
            )
        except Exception as e:
            raise InvalidArgument(str(e))
        return _schedules

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
        if cloud:
            query = query.join(Assignment).filter(Assignment.cloud == cloud)
        if not date:
            date = datetime.now()
        query = query.filter(and_(Schedule.start <= date, Schedule.end >= date))

        if host:
            query = query.filter(Schedule.host == host)

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
