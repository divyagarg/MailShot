import logging
from datetime import datetime
from flask import g

from redis import Redis
from rq_scheduler import Scheduler

from sqlalchemydb import AlchemyDB
from api.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_QUEUE
from smtp import async_mail_sender
from segment import Segment


logger = logging.getLogger()
scheduler = Scheduler(connection=Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB), queue_name=REDIS_QUEUE)


class Campaign:

    def __init__(self, id=None, name=None, status=None, send_time=None, categoryid=None, templateid=None, segment_list=None):
        self.id = id
        self.name = name
        self.status = status
        self.send_time = datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S') if send_time else datetime.now()
        self.categoryid = categoryid
        self.templateid = templateid
        logger.debug(segment_list)
        if segment_list:
            self.segment_list = [Segment(id=s) for s in segment_list]

    def save_campaign(self):
        db = AlchemyDB()
        db.begin()
        try:
            self.id = db.insert_row("Campaign", Name=self.name, CategoryId=self.categoryid, SendTime=self.send_time,
                                    TemplateId=self.templateid)
            segment_data = [{"CampaignId": self.id, "SegmentId": s.id} for s in self.segment_list]
            db.insert_row_batch("CampaignSegmentMap", segment_data)
            logger.debug(self.id)
        except Exception as e:
            db.rollback()
            logger.exception(e)
        else:
            db.commit()
        self._schedule_campaign()

    def _schedule_campaign(self):
        scheduler.enqueue_at(self.send_time, async_mail_sender, self)
        logger.debug(scheduler.get_jobs())

    def to_json(self):
        d = {k: v for k , v in self.__dict__.iteritems() if k!='segment_list'}
        logger.debug(self.segment_list)
        d["segment_list"] = [s.to_json() for s in self.segment_list]
        return d

    def get_campaigns_list(self, limit, offset):
        logger.debug("%s getting_Campains for limit %s and offset %s", g.UUID, limit, offset)
        db = AlchemyDB()
        try:
            campaigns = db.find(table_name="Campaign", _limit=limit, _offset=offset)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            raise exception
        else:
            return campaigns

    def find_campaign(self, **filter):
        logger.debug('%s Getting campaign for campaign id %s', g.UUID, self.id)
        db = AlchemyDB()
        join_list = []
        try:
            for column, value in filter.iteritems():
                if value:
                    join_list.append({"Campaign" + '.' + column : value})
            campaign = db.select_join(["Campaign", "CampaignSegmentMap", "Segment"], [{"Id": "CampaignId"}, {"SegmentId": "Id"}], [join_list], joinflag="outer")
        except Exception as exception:
            logger.error("in exception")
            logger.error(exception)
            raise exception
        else:
            self.load_campaign_details(campaign)
            return True

    def load_campaign_details(self, details):
        self.name, self.status, self.send_time, self.categoryid, self.templateid = details[0]["Campaign_Name"], details[0]["Campaign_Status"], \
                                                                                   details[0]["Campaign_SendTime"], details[0]["Campaign_CategoryId"], details[0]["Campaign_TemplateId"]

        self.segment_list = []
        for d in details:
            self.segment_list.append(Segment(d["Segment_Id"], d["Segment_Name"]))









