import logging
import binascii

from app.src.sqlalchemydb import AlchemyDB

logger = logging.getLogger()


def insert_open_tracking_details(user_tracker_id, campaignid, contactid, variantid):
    db = AlchemyDB()
    tracker_id = binascii.a2b_hex(user_tracker_id)
    db.insert_row("MailTrack", UserTrackerId=tracker_id, CampaignId=campaignid, ContactId=contactid, VariantId=variantid)


def insert_click_tracking_details(user_tracker_id, link_map):
    tracker_id = binascii.a2b_hex(user_tracker_id)
    data = [{"UserTrackerTid": tracker_id, "Link": k , "RedirectId": v} for k, v in link_map.iteritems()]
    db = AlchemyDB()
    db.insert_row_batch("LinkTrack",data)