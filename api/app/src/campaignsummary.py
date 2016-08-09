import logging
from app.src.sqlalchemydb import AlchemyDB
from flask import g

__author__ = 'divyagarg'

logger = logging.getLogger()

class CampaignSummary(object):

    def __init__(self, campaign_id=None, contact_count = None, click_count=None, unique_click_count = None, open_count = None, bounce_count = None, spam_count = None, vaiant_id = None):
        self.campaignId = campaign_id
        self.contactCount = contact_count
        self.clickCount = click_count
        self.uniqueClickCount = unique_click_count
        self.openCount = open_count
        self.bounceCount = bounce_count
        self.spamCount = spam_count
        self.variantId = vaiant_id

    def get_campaign_summary(self):
        logger.debug("%s Getting Campign Summary for campign id %s", g.UUID, self.campaignId)
        db = AlchemyDB()
        try:
            campaignSummary = db.find(table_name="CampaignSummary", CampaignId = self.campaignId)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        else:
            return campaignSummary


