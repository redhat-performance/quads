from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Processor


class ProcessorDao(BaseDao):
    @staticmethod
    def get_processors() -> List[Processor]:
        processors = db.session.query(Processor).all()
        return processors

    @staticmethod
    def get_processor(processor_id: int) -> Processor:
        processor = (
            db.session.query(Processor).filter(Processor.id == processor_id).first()
        )
        return processor
