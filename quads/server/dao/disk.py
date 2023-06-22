from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Disk


class DiskDao(BaseDao):
    @staticmethod
    def get_disks() -> List[Disk]:
        disks = db.session.query(Disk).all()
        return disks

    @staticmethod
    def get_disk(disk_id: int) -> Disk:
        disk = db.session.query(Disk).filter(Disk.id == disk_id).first()
        return disk
