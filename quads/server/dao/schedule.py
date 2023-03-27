from datetime import datetime
from typing import List
from sqlalchemy import and_, or_

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.host import HostDao
from quads.server.models import db, Host, Schedule, Cloud


class ScheduleDao(BaseDao):
    @staticmethod
    def get_schedules() -> List[Schedule]:
        schedules = db.session.query(Schedule).all()
        return schedules

    @staticmethod
    def get_schedule(schedule_id) -> Schedule:
        schedules = (
            db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
        )
        return schedules

    @staticmethod
    def get_future_schedules(host: Host = None, cloud: Cloud = None) -> List[Schedule]:
        now = datetime.now()
        query = db.session.query(Schedule).filter(Schedule.end >= now)
        if host:
            query = query.filter(Schedule.host == host)
        if cloud:
            assignments = AssignmentDao.get_all_cloud_assignments(cloud)
            # TODO: check or_ construction

            query = query.filter(
                or_([Schedule.assignment == ass for ass in assignments])
            )
        return query.all()

    @staticmethod
    def get_current_schedule(
        date: datetime = None, host: Host = None, cloud: Cloud = None
    ) -> List[Schedule]:
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
        return query.all()

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
            query = query.filter(Schedule.index != exclude)
        results = query.all()
        for result in results:
            if result.start <= start < result.end:
                return False
            if result.start < end <= result.end:
                return False
            if start < result.start and end > result.end:
                return False

        return True
