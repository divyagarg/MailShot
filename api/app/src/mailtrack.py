import logging
import binascii
from app.src.sqlalchemydb import AlchemyDB
from flask import g

__author__ = 'divyagarg'

logger = logging.getLogger()
class MailTrack(object):

    def __init__(self, id = None,
                 user_tracker_id = None,
                 campaignId = None,
                 contactId=None,
                 openStatus = None,
                 deliveryStatus = None,
                 bounceStatus = None,
                 isSpam = False,
                 isSample = False,
                 variantid = None
                 ):
        self.id = id
        self.user_tracker_id = user_tracker_id
        self.campaignId = campaignId
        self.contactId = contactId
        self.openStatus = openStatus
        self.deliveryStatus = deliveryStatus
        self.bounceStatus = bounceStatus
        self.isSpam = isSpam
        self.isSample = isSample
        self.variantid = variantid


    def update_open_status(self):
        logger.debug("%s Updating open Email Status for usertracking id  %s", g.UUID, self.user_tracker_id)
        db = AlchemyDB()
        db.begin()

        try:
            usertrackerid = binascii.a2b_hex(self.user_tracker_id)
            where = {'UserTrackerId': usertrackerid}
            val = dict()
            val['OpenStatus'] = 1
            result = db.update_row_new(table_name = "MailTrack", where= where, val = val)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        if result:
            db.commit()
        return result

    def update_unsubscription_status(self):
        logger.debug("%s Updating Unsubscribe status for usertracking id  %s", g.UUID, self.user_tracker_id)
        db = AlchemyDB()
        db.begin()
        try:
            usertrackerid = binascii.a2b_hex(self.user_tracker_id)
            mailtracker = db.find_one("MailTrack", UserTrackerId = usertrackerid)
            contactId = mailtracker.get('ContactId')
            val = {'SubscriptionStatus': 0}
            where = {'ContactId': contactId}
            result = db.update_row_new("ContactInfo", where = where, val = val)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        if result:
            db.commit()
        return result