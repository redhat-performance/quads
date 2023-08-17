from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.host import HostDao
from quads.server.models import db, Memory


class MemoryDao(BaseDao):
    @staticmethod
    def create_memory(hostname: str, handle: str, size_gb: int) -> Memory:
        _host_obj = HostDao.get_host(hostname)
        if not _host_obj:
            raise EntryNotFound
        _memory = Memory(
            handle=handle,
            size_gb=size_gb,
            host_id=_host_obj.id,
        )
        db.session.add(_memory)
        db.session.commit()
        return _memory

    @staticmethod
    def get_memories() -> List[Memory]:
        memories = db.session.query(Memory).all()
        return memories

    @staticmethod
    def get_memory(memory_id: int) -> Memory:
        memory = db.session.query(Memory).filter(Memory.id == memory_id).first()
        return memory

    @staticmethod
    def get_memory_for_host(host_id: int) -> [Memory]:
        memories = db.session.query(Memory).filter(Memory.host_id == host_id).all()
        return memories
