from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Memory


class MemoryDao(BaseDao):
    @staticmethod
    def get_memories() -> List[Memory]:
        memories = db.session.query(Memory).all()
        return memories

    @staticmethod
    def get_memory(memory_id: int) -> Memory:
        memory = db.session.query(Memory).filter(Memory.id == memory_id).first()
        return memory
