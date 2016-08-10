import logging

from app.src.sqlalchemydb import AlchemyDB
from flask import g


__author__ = 'divyagarg'

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
    def get_email_list(segment_list):
        db = AlchemyDB()
        data = db.select_join(["Segment", "ContactSegmentMao", "ContactInfo"], [{"Id": "SegmentId"}, {"ContactId": "Id"}], [[{"Segment.Id": segment_list}]])
        email = set()
        for d in data:
            email.add(d["ContactInfo.Email"])
        return list(email)