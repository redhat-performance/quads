from typing import List, Optional, Type

from sqlalchemy import Boolean
from sqlalchemy.orm import RelationshipProperty

from quads.config import Config
from quads.server.dao.baseDao import BaseDao, OPERATORS, MAP_MODEL, EntryNotFound, EntryExisting
from quads.server.dao.cloud import CloudDao
from quads.server.models import db, Host, Cloud


class HostDao(BaseDao):
    @classmethod
    def create_host(cls, name, model, host_type, default_cloud) -> Host:
        _host_obj = cls.get_host(name)
        if _host_obj:
            raise EntryExisting
        if not default_cloud:
            default_cloud = Config["spare_pool_name"]
        _default_cloud_obj = CloudDao.get_cloud(default_cloud)
        if not _default_cloud_obj:
            raise EntryNotFound(f"Default cloud not found: {default_cloud}")
        _host = Host(name=name, model=model, host_type=host_type, default_cloud=_default_cloud_obj)
        db.session.add(_host)
        db.session.commit()
        return _host

    @classmethod
    def remove_host(cls, name) -> None:
        _host_obj = cls.get_host(name)
        if not _host_obj:
            raise EntryNotFound
        db.session.delete(_host_obj)
        db.session.commit()
        return

    @staticmethod
    def get_host(hostname) -> Optional[Host]:
        host = db.session.query(Host).filter(Host.name == hostname).first()
        return host

    @staticmethod
    def get_hosts() -> List[Type[Host]]:
        hosts = db.session.query(Host).all()
        return hosts

    @staticmethod
    def filter_hosts_dict(data):
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

            field = Host.__mapper__.attrs.get(first_field)

            if (
                type(field) != RelationshipProperty
                and type(field.columns[0].type) == Boolean
            ):
                value = value.lower() in ["true", "y", 1, "yes"]
            else:
                if first_field in ["cloud", "default_cloud"]:
                    cloud = CloudDao.get_cloud(value)
                    if not cloud:
                        raise EntryNotFound(f"Could not find cloud: {value}")
                    value = cloud
                if first_field.lower() in MAP_MODEL.keys():
                    if len(fields) > 1:
                        field_name = f"{first_field.lower()}.{field_name.lower()}"
            filter_tuples.append(
                (
                    field_name,
                    operator,
                    value,
                )
            )
        if filter_tuples:
            _hosts = HostDao.create_query_select(Host, filters=filter_tuples)
        else:
            _hosts = HostDao.get_hosts()
        return _hosts

    @staticmethod
    def filter_hosts(
        model: str = None,
        host_type: str = None,
        build: bool = None,
        validated: bool = None,
        switch_config_applied: bool = None,
        broken: bool = None,
        retired: bool = None,
        cloud: Cloud = None,
        default_cloud: Cloud = None,
    ) -> List[Host]:
        query = db.session.query(Host)
        if model:
            query.filter(Host.model == model)
        if host_type:
            query.filter(Host.host_type == host_type)
        if build is not None:
            query.filter(Host.build == build)
        if validated is not None:
            query.filter(Host.validated == validated)
        if switch_config_applied is not None:
            query.filter(Host.switch_config_applied == switch_config_applied)
        if broken is not None:
            query.filter(Host.broken == broken)
        if retired is not None:
            query.filter(Host.retired == retired)
        if cloud:
            query.filter(Host.cloud == cloud)
        if default_cloud:
            query.filter(Host.default_cloud == default_cloud)
        hosts = query.all()
        return hosts
