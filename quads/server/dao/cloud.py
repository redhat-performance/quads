from typing import List, Optional, Type

from sqlalchemy import Boolean
from sqlalchemy.orm import RelationshipProperty, Relationship

from quads.server.dao.baseDao import (
    BaseDao,
    EntryExisting,
    EntryNotFound,
    OPERATORS,
    InvalidArgument,
)
from quads.server.models import db, Cloud


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
    def get_clouds() -> List[Type[Cloud]]:
        clouds = db.session.query(Cloud).all()
        return clouds

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
            if (
                type(field) != RelationshipProperty
                and type(field) != Relationship
                and type(field.columns[0].type) == Boolean
            ):
                value = value.lower() in ["true", "y", 1, "yes"]
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
