import logging

from app.src.sqlalchemydb import AlchemyDB
from flask import g


logger = logging.getLogger()


class Segment(object):
    def __init__(self, id= None, name=None):
        self.name = name
        self.id = id

    def get_all_segments(self):
        logger.debug("%s getting_Segments", g.UUID)
        db = AlchemyDB()

        try:
            segments = db.find(table_name="Segment")
        except Exception as exception:
            logger.error(exception, exc_info=True)
            raise exception
        else:
            segment_list = []
            for each_segment in segments:
                segment_map = {}
                segment_map['id'] = each_segment.get('Id')
                segment_map['name'] = each_segment.get('Name')
                segment_list.append(segment_map)
            return segment_list

    def to_json(self):
        return self.__dict__

    @staticmethod
    def get_contact_list(segment_list):
        db = AlchemyDB()
        where = []
        where.append({"Segment.Id": segment_list})
        data = db.select_join(["Segment", "ContactSegmentMap", "ContactInfo"], [{"Id": "SegmentId"}, {"ContactId": "ContactId"}], [where])
        email = set()
        contactinfo = []
        for d in data:
            if d["ContactInfo_Email"] not in email:
                email.add(d["ContactInfo_Email"])
                contactinfo.append({"email": d["ContactInfo_Email"], "contactid": d["ContactInfo_ContactId"]})
        return contactinfo