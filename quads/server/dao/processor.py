from typing import List

from quads.server.dao.baseDao import BaseDao, EntryNotFound
from quads.server.dao.host import HostDao
from quads.server.models import db, Processor


class ProcessorDao(BaseDao):
    @staticmethod
    def create_processor(
        hostname: str, handle: str, vendor: str, product: str, cores: int, threads: int
    ) -> Processor:
        _host_obj = HostDao.get_host(hostname)
        if not _host_obj:
            raise EntryNotFound
        _processor = Processor(
            handle=handle,
            vendor=vendor,
            product=product,
            cores=cores,
            threads=threads,
            host_id=_host_obj.id,
        )
        db.session.add(_processor)
        db.session.commit()
        return _processor

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

    @staticmethod
    def get_processor_for_host(host_id: int) -> [Processor]:
        processors = (
            db.session.query(Processor).filter(Processor.host_id == host_id).all()
        )
        return processors
