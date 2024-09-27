from datetime import datetime
from typing import List, Optional, Type

from sqlalchemy import Boolean, and_

from quads.server.dao.baseDao import (
    OPERATORS,
    BaseDao,
    EntryExisting,
    EntryNotFound,
    InvalidArgument,
)
from quads.server.models import Assignment, Cloud, Schedule, db
from quads.config import Config


class CloudDao(BaseDao):
    @classmethod
    def create_cloud(cls, name) -> Cloud:
        _cloud_obj = cls.get_cloud(name)
        if _cloud_obj:
            raise EntryExisting
        _cloud = Cloud(name=name)
        db.session.add(_cloud)
        cls.safe_commit()
        return _cloud

    @classmethod
    def update_cloud(cls, cloud_name: str, **kwargs) -> Cloud:  # pragma: no cover
        """
        Updates a cloud in the database.

        :param self: Represent the instance of the class
        :param name: str: Cloud name
        :param last_redefined: datetime: Last time the cloud was redefined

        :return: The updated assignment
        """
        cloud = cls.get_cloud(cloud_name)
        if not cloud:
            raise EntryNotFound

        for key, value in kwargs.items():

            if getattr(cloud, key):
                setattr(cloud, key, value)
            else:
                raise InvalidArgument

        cls.safe_commit()

        return cloud

    @classmethod
    def remove_cloud(cls, name) -> None:
        _cloud_obj = cls.get_cloud(name)
        if not _cloud_obj:
            raise EntryNotFound
        db.session.delete(_cloud_obj)
        cls.safe_commit()
        return

    @staticmethod
    def get_cloud(name) -> Optional[Cloud]:
        cloud = db.session.query(Cloud).filter(Cloud.name == name).first()
        return cloud

    @staticmethod
    def get_clouds() -> List[Cloud]:
        clouds = db.session.query(Cloud).order_by(Cloud.name.asc()).all()
        return clouds

    @staticmethod
    def get_free_clouds() -> List[Cloud]:
        free_clouds = (
            db.session.query(Cloud)
            .outerjoin(Assignment, Cloud.id == Assignment.cloud_id)
            .outerjoin(Schedule, Assignment.id == Schedule.assignment_id)
            .filter(and_(Cloud.name != Config["spare_pool_name"], Schedule.end <= datetime.now()))
            .order_by(Cloud.name.asc())
            .distinct()
            .all()
        )
        return free_clouds

    @staticmethod
    def filter_clouds_dict(data: dict) -> List[Type[Cloud]]:
        filter_tuples = []
        operator = "=="
        for k, value in data.items():
            fields = k.split(".")

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

            field = Cloud.__mapper__.attrs.get(first_field)
            if not field:
                raise InvalidArgument(f"{k} is not a valid field.")
            try:
                if type(field.columns[0].type) == Boolean:
                    value = value.lower() in ["true", "y", 1, "yes"]
            except AttributeError:
                pass
            filter_tuples.append(
                (
                    field_name,
                    operator,
                    value,
                )
            )
        if filter_tuples:
            _clouds = CloudDao.create_query_select(Cloud, filters=filter_tuples)
        else:
            _clouds = CloudDao.get_clouds()
        return _clouds
