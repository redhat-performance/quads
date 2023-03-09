from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Disk, Interface


class InterfaceDao(BaseDao):
    @staticmethod
    def get_interfaces() -> List[Interface]:
        interfaces = db.session.query(Interface).all()
        return interfaces

    @staticmethod
    def get_interface(interface_id: int) -> Interface:
        interface = (
            db.session.query(Interface).filter(Interface.id == interface_id).first()
        )
        return interface
