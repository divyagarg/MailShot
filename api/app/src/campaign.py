import logging
from datetime import datetime

from redis import Redis
from rq_scheduler import Scheduler

from sqlalchemydb import AlchemyDB
from api.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_QUEUE
from smtp import async_mail_sender


logger = logging.getLogger()
scheduler = Scheduler(connection=Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB), queue_name=REDIS_QUEUE)


class Campaign:
    def __init__(self, id=None, name=None, status=None, send_time=None, categoryid=None, templateid=None):
        self.id = id
        self.name = name
        self.status = status
        self.send_time = datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S') if send_time else datetime.now()
        self.categoryid = categoryid
        self.templateid = templateid

    def save_campaign(self):
        db = AlchemyDB()
        self.id = db.insert_row("Campaign", Name=self.name, CategoryId=self.categoryid, SendTime=self.send_time,
                                TemplateId=self.templateid)
        logger.debug(self.id)
        self._schedule_campaign()

    def _schedule_campaign(self):
        scheduler.enqueue_at(self.send_time, async_mail_sender, self)
        logger.debug(scheduler.get_jobs())

    def to_json(self):
        return self.__dict__






