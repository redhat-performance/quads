from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Host


class HostDao(BaseDao):
    @staticmethod
    def get_host(hostname) -> Host:
        host = db.session.query(Host).filter(Host.name == hostname).first()
        return host

    @staticmethod
    def get_hosts() -> List[Host]:
        hosts = db.session.query(Host).all()
        return hosts
