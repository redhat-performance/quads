from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Vlan


class VlanDao(BaseDao):
    @staticmethod
    def get_vlan(vlan_id: str) -> Vlan:
        cloud = db.session.query(Vlan).filter(Vlan.vlan_id == vlan_id).first()
        return cloud

    @staticmethod
    def get_vlans() -> List[Vlan]:
        # TODO:Union with assignments table on assignments.vlan_id=Vlan.vlan_id where assignments.active=True
        # to include a column with the assignment ID
        vlans = db.session.query(Vlan).all()
        return vlans
