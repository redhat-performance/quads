from typing import List

from quads.server.dao.baseDao import BaseDao
from quads.server.models import db, Notification


class NotificationDao(BaseDao):
    @staticmethod
    def get_notifications() -> List[Notification]:
        notifications = db.session.query(Notification).all()
        return notifications

    @staticmethod
    def get_notification(notification_id: int) -> Notification:
        processor = db.session.query(Notification).filter(Notification.id == notification_id).first()
        return processor

    @staticmethod
    def get_assignment_notification(assignment_id: int) -> Notification:
        processors = db.session.query(Notification).filter(Notification.assignment_id == assignment_id).first()
        return processors
