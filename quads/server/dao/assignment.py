from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import db, Assignment, Cloud, Notification, Vlan
from sqlalchemy import and_


class AssignmentDao(BaseDao):
    @staticmethod
    def create_assignment(
            description: str,
            owner: str,
            ticket: str,
            qinq: int,
            wipe: bool,
            ccuser: list[str],
            vlan_id: int,
            cloud: str,
    ) -> Assignment:
        vlan = VlanDao.get_vlan(vlan_id)
        cloud = CloudDao.get_cloud(cloud)
        notification = Notification()
        try:
            _assignment_obj = Assignment(
                description=description,
                owner=owner,
                ticket=ticket,
                qinq=qinq,
                wipe=wipe,
                ccuser=ccuser,
                vlan=vlan,
                cloud=cloud,
                notification=notification,
            )
        except Exception as ex:
            print(ex)
        db.session.add(_assignment_obj)
        db.session.commit()

        return _assignment_obj

    @staticmethod
    def get_assignment(assignment_id: int) -> Assignment:
        assignment = (
            db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        )
        if assignment and not assignment.notification:
            assignment.notification = (
                db.session.query(Notification)
                .filter(Assignment.id == assignment_id)
                .first()
            )
        return assignment

    @classmethod
    def remove_assignment(cls, assignment_id) -> None:
        _assignments_obj = cls.get_assignment(assignment_id)
        if not _assignments_obj:
            raise EntryNotFound
        db.session.delete(_assignments_obj)
        db.session.commit()
        return

    @staticmethod
    def get_assignments() -> List[Assignment]:
        assignment = db.session.query(Assignment).all()
        if assignment:
            for a in assignment:
                if not a.notification:
                    a.notification = (
                        db.session.query(Notification)
                        .filter(Assignment.id == a.id)
                        .first()
                    )
        return assignment

    @staticmethod
    def get_all_cloud_assignments(cloud: Cloud) -> List[Assignment]:
        assignments = (
            db.session.query(Assignment).filter(Assignment.cloud == cloud).all()
        )
        return assignments

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
