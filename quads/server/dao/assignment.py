from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Cloud, Assignment


class AssignmentDao(BaseDao):
    @staticmethod
    def get_cloud_assignment(cloud_name) -> Assignment:
        assignment = (
            db.session.query(Assignment)
            .filter(Assignment.cloud.name == cloud_name)
            .first()
        )
        return assignment
