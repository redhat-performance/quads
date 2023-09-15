from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.host import HostDao
from quads.server.models import db, Disk


class DiskDao(BaseDao):
    @classmethod
    def create_disk(
        cls,
        hostname: str,
        disk_type: str,
        size_gb: int,
        count: int,
    ) -> Disk:
        _host_obj = HostDao.get_host(hostname)
        if not _host_obj:
            raise EntryNotFound
        _disk = Disk(
            disk_type=disk_type,
            size_gb=size_gb,
            count=count,
            host_id=_host_obj.id,
        )
        db.session.add(_disk)
        cls.safe_commit()
        return _disk

    @staticmethod
    def get_disks() -> List[Disk]:
        disks = db.session.query(Disk).all()
        return disks

    @staticmethod
    def get_disk(disk_id: int) -> Disk:
        disk = db.session.query(Disk).filter(Disk.id == disk_id).first()
        return disk
