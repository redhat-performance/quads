from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound, InvalidArgument
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import db, Assignment, Cloud, Notification
from sqlalchemy import and_


class AssignmentDao(BaseDao):
    @staticmethod
    def create_assignment(
            description: str,
            owner: str,
            ticket: str,
            qinq: int,
            wipe: bool,
            ccuser: List[str],
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

    @classmethod
    def udpate_assignment(
            cls,
            assignment_id: int,
            **kwargs
    ) -> Assignment:
        """
        Updates an assignment in the database.

        :param self: Represent the instance of the class
        :param assignment_id: int: Identify the assignment to be updated
        :param description: str: Pass a string to the assignment description field
        :param owner: str: Set the owner of the assignment
        :param ticket: str: Update the ticket field in the assignment table
        :param qinq: int: Set the qinq value for an assignment
        :param wipe: bool: Wipe the assignment
        :param ccuser: list[str]: Add multiple cc_users to the assignment
        :param vlan_id: int: Set the vlan of an assignment
        :param cloud: str: Set the cloud attribute of an assignment
        :param active: bool: Set the assignment to active or inactive

        :return: The updated assignment
        """
        assignment = cls.get_assignment(assignment_id)
        if not assignment:
            raise EntryNotFound

        for key, value in kwargs.items():
            if key == "vlan_id":
                vlan = VlanDao.get_vlan(value)
                if not vlan:
                    raise EntryNotFound
                assignment.vlan = vlan
                continue

            if key == "cloud":
                cloud = CloudDao.get_cloud(value)
                if not cloud:
                    raise EntryNotFound
                assignment.cloud = cloud
                continue

            if getattr(assignment, key):
                setattr(assignment, key, value)
            else:
                raise InvalidArgument

        db.session.commit()

        return assignment

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
    def get_active_assignments() -> List[Assignment]:
        assignments = (
            db.session.query(Assignment)
            .filter(Assignment.active == True)
            .all()
        )
        return assignments

    @staticmethod
    def delete_assignment(assignment_id: int):
        _assignment_obj = (
            db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        )

        if not _assignment_obj:
            raise EntryNotFound(f"Could not find assignment with id: {assignment_id}")

        db.session.delete(_assignment_obj)
        db.session.commit()
