import logging

from app.src.sqlalchemydb import AlchemyDB
from flask import g


__author__ = 'divyagarg'

logger = logging.getLogger()

class Segment(object):
    def __init__(self, name=None):
        self.name = name
        self.id = None

    def get_all_segments(self):
        logger.debug("%s getting_Segments", g.UUID)
        db = AlchemyDB()

        try:
            segments = db.find("Segment")
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        else:
            return segments
