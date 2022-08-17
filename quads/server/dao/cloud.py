from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Cloud


class CloudDao(BaseDao):
    @staticmethod
    def get_cloud(name) -> Cloud:
        cloud = db.session.query(Cloud).filter(Cloud.name == name).first()
        return cloud

    @staticmethod
    def get_clouds() -> List[Cloud]:
        clouds = db.session.query(Cloud).all()
        return clouds
