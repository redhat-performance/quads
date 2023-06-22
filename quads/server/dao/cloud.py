from typing import List, Optional, Type

from quads.server.dao.baseDao import BaseDao, EntryExisting, EntryNotFound
from quads.server.models import db, Cloud


class CloudDao(BaseDao):
    @classmethod
    def create_cloud(cls, name) -> Cloud:
        _cloud_obj = cls.get_cloud(name)
        if _cloud_obj:
            raise EntryExisting
        _cloud = Cloud(name=name)
        db.session.add(_cloud)
        db.session.commit()
        return _cloud

    @classmethod
    def remove_cloud(cls, name) -> None:
        _cloud_obj = cls.get_cloud(name)
        if not _cloud_obj:
            raise EntryNotFound
        db.session.delete(_cloud_obj)
        db.session.commit()
        return

    @staticmethod
    def get_cloud(name) -> Optional[Cloud]:
        cloud = db.session.query(Cloud).filter(Cloud.name == name).first()
        return cloud

    @staticmethod
    def get_clouds() -> List[Type[Cloud]]:
        clouds = db.session.query(Cloud).all()
        return clouds
