from datetime import datetime
from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Host, Cloud, Interface, Disk, Memory, Processor


class HostDao(BaseDao):
    @staticmethod
    def get_host(hostname) -> Host:
        host = db.session.query(Host).filter(Host.name == hostname).first()
        return host

    @staticmethod
    def get_hosts() -> List[Host]:
        hosts = db.session.query(Host).all()
        return hosts

    @staticmethod
    def filter_hosts(
        model: str = None,
        host_type: str = None,
        build: bool = None,
        validated: bool = None,
        switch_config_applied: bool = None,
        broken: bool = None,
        retired: bool = None,
        # last_build: datetime = None,
        cloud: Cloud = None,
        default_cloud: Cloud = None,
        # interfaces: Interface = None,
        # disks: Disk = None,
        # memory: Memory = None,
        # processors: Processor = None,
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
