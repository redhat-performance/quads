from typing import List, Type

from quads.server.dao.baseDao import (
    BaseDao,
    EntryNotFound,
    InvalidArgument,
    OPERATORS,
)
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import db, Assignment, Cloud, Notification
from sqlalchemy import and_, Boolean
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.relationships import Relationship


class AssignmentDao(BaseDao):
    @classmethod
    def create_assignment(
        cls,
        description: str,
        owner: str,
        ticket: str,
        qinq: int,
        wipe: bool,
        ccuser: List[str],
        cloud: str,
        vlan_id: int = None,
    ) -> Assignment:
        cloud = CloudDao.get_cloud(cloud)
        notification = Notification()
        kwargs = {
            "description": description,
            "owner": owner,
            "ticket": ticket,
            "qinq": qinq,
            "wipe": wipe,
            "ccuser": ccuser,
            "cloud": cloud,
            "notification": notification,
        }
        if vlan_id:
            vlan = VlanDao.get_vlan(vlan_id)
            if vlan:
                kwargs["vlan"] = vlan
        try:
            _assignment_obj = Assignment(**kwargs)
        except Exception as ex:
            print(ex)
        db.session.add(_assignment_obj)
        cls.safe_commit()

        return _assignment_obj

    @classmethod
    def udpate_assignment(cls, assignment_id: int, **kwargs) -> Assignment:
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

        cls.safe_commit()

        return assignment

    @staticmethod
    def get_assignment(assignment_id: int) -> Assignment:
        assignment = db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        if assignment and not assignment.notification:
            assignment.notification = db.session.query(Notification).filter(Assignment.id == assignment_id).first()
        return assignment

    @classmethod
    def remove_assignment(cls, assignment_id) -> None:
        _assignments_obj = cls.get_assignment(assignment_id)
        if not _assignments_obj:
            raise EntryNotFound
        db.session.delete(_assignments_obj)
        cls.safe_commit()
        return

    @staticmethod
    def get_assignments() -> List[Assignment]:
        assignment = db.session.query(Assignment).all()
        if assignment:
            for a in assignment:
                if not a.notification:
                    a.notification = db.session.query(Notification).filter(Assignment.id == a.id).first()
        return assignment

    @staticmethod
    def filter_assignments(data: dict) -> List[Type[Assignment]]:
        filter_tuples = []
        operator = "=="
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

            field = Assignment.__mapper__.attrs.get(first_field)
            if not field:
                raise InvalidArgument(f"{k} is not a valid field.")
            if (
                type(field) != RelationshipProperty
                and type(field) != Relationship
                and type(field.columns[0].type) == Boolean
            ):
                value = str(value).lower() in ["true", "y", 1, "yes"]
            else:
                if first_field in ["cloud"]:
                    cloud = CloudDao.get_cloud(value)
                    if not cloud:
                        raise EntryNotFound(f"Cloud not found: {value}")
                    value = cloud
            filter_tuples.append(
                (
                    field_name,
                    operator,
                    value,
                )
            )
        if filter_tuples:
            _hosts = AssignmentDao.create_query_select(Assignment, filters=filter_tuples)
        else:
            _hosts = AssignmentDao.get_assignments()
        return _hosts

    @staticmethod
    def get_all_cloud_assignments(cloud: Cloud) -> List[Assignment]:
        assignments = db.session.query(Assignment).filter(Assignment.cloud == cloud).all()
        return assignments

    @staticmethod
    def get_active_cloud_assignment(cloud: Cloud) -> Assignment:
        assignment = (
            db.session.query(Assignment).filter(and_(Assignment.cloud == cloud, Assignment.active == True)).first()
        )
        return assignment

    @staticmethod
    def get_active_assignments() -> List[Assignment]:
        assignments = db.session.query(Assignment).filter(Assignment.active == True).all()
        return assignments

    @classmethod
    def delete_assignment(cls, assignment_id: int):
        _assignment_obj = db.session.query(Assignment).filter(Assignment.id == assignment_id).first()

        if not _assignment_obj:
            raise EntryNotFound(f"Could not find assignment with id: {assignment_id}")

        db.session.delete(_assignment_obj)
        cls.safe_commit()
