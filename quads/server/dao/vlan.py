from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Vlan


class VlanDao(BaseDao):
    @staticmethod
    def get_vlan(vlan_id) -> Vlan:
        cloud = db.session.query(Vlan).filter(Vlan.vlan_id == vlan_id).first()
        return cloud

    @staticmethod
    def get_vlans() -> List[Vlan]:
        vlans = db.session.query(Vlan).all()
        return vlans
