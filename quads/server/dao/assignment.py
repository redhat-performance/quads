from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.cloud import CloudDao
from quads.server.models import db, Cloud, Assignment
from sqlalchemy import and_


class AssignmentDao(BaseDao):
    @staticmethod
    def get_cloud_assignments(cloud_name) -> Assignment:
        cloud = CloudDao.get_cloud(cloud_name)
        assignment = (
            db.session.query(Assignment).filter(Assignment.cloud == cloud).first()
        )
        return assignment

    @staticmethod
    def get_active_cloud_assignment(cloud_name) -> Assignment:
        cloud = CloudDao.get_cloud(cloud_name)
        assignment = (
            db.session.query(Assignment)
            .filter(and_(Assignment.cloud == cloud, Assignment.active == True))
            .first()
        )
        return assignment

    @staticmethod
    def delete_assignment(assignment_id):
        _assignment_obj = (
            db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        )

        if not _assignment_obj:
            raise EntryNotFound(f"Could not find assignment with id: {assignment_id}")

        db.session.delete(_assignment_obj)
        db.session.commit()
