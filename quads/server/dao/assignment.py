from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.models import db, Assignment, Cloud, Notification
from sqlalchemy import and_


class AssignmentDao(BaseDao):
    @staticmethod
    def get_assignment(assignment_id: int) -> Assignment:
        assignment = (
            db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        )
        if assignment and not assignment.notification:
            assignment.notification = db.session.query(Notification).filter(Assignment.id == assignment_id).first()
        return assignment

    @staticmethod
    def get_assignments() -> List[Assignment]:
        assignment = db.session.query(Assignment).all()
        if assignment:
            for a in assignment:
                if not a.notification:
                    a.notification = db.session.query(Notification).filter(Assignment.id == a.id).first()
        return assignment

    @staticmethod
    def get_all_cloud_assignments(cloud: Cloud) -> List[Assignment]:
        assignment = db.session.query(Assignment).filter(Assignment.cloud == cloud).all()
        return assignment.all()

    @staticmethod
    def get_active_cloud_assignment(cloud: Cloud) -> Assignment:
        assignment = (
            db.session.query(Assignment)
            .filter(and_(Assignment.cloud == cloud, Assignment.active == True))
            .first()
        )
        return assignment

    @staticmethod
    def delete_assignment(assignment_id: int):
        _assignment_obj = (
            db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        )

        if not _assignment_obj:
            raise EntryNotFound(f"Could not find assignment with id: {assignment_id}")

        db.session.delete(_assignment_obj)
        db.session.commit()
