from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.host import HostDao
from quads.server.models import db, Disk, Interface


class InterfaceDao(BaseDao):
    @staticmethod
    def create_interface(hostname: str, name: str, bios_id: str, mac_address: str, switch_ip: str, switch_port: str, speed: int, vendor: str, pxe_boot: bool, maintenance: str) -> Interface:
        _host_obj = HostDao.get_host(hostname)
        if not _host_obj:
            raise EntryNotFound
        _interface = Interface(
            name=name,
            bios_id=bios_id,
            mac_address=mac_address,
            switch_ip=switch_ip,
            switch_port=switch_port,
            speed=speed,
            vendor=vendor,
            pxe_boot=pxe_boot,
            maintenance=maintenance,
            host_id=_host_obj.id,
        )
        db.session.add(_interface)
        db.session.commit()
        return _interface

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
