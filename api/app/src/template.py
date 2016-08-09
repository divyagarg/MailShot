import logging
from app.src.sqlalchemydb import AlchemyDB

__author__ = 'divyagarg'

logger = logging.getLogger()

class Template(object):
    def __init__(self, name=None, userid=None):
        self.name = name
        self.userid = userid
        self.id = None

    def save_template(self):
        logger.debug("%s Insert_Template", g.UUID)
        db = AlchemyDB()
        db.begin()
        try:
            args = {"Name": self.name, "UserId": self.userid}
            self.id = db.insert_row("Template", **args)
            logger.debug(self.id)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        else:
            db.commit()
        return self.id

    def to_json(self):
        return self.__dict__

