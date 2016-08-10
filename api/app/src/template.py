import logging

from flask import g

from app.src.sqlalchemydb import AlchemyDB
from variant import Variant


logger = logging.getLogger()


class Template(object):
    def __init__(self, id=None, name=None, userid=None):
        self.name = name
        self.userid = userid
        self.id = id
        self.varaint_list = None

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

    def get_template(self):
        db = AlchemyDB()
        join_list = []
        try:
            join_list.append({"Template" + '.' + "Id" : self.id})
            template = db.select_join(["Template", "Variant"], [{"Id": "TemplateId"}], [join_list])
        except Exception as exception:
            logger.error("in exception")
            logger.error(exception)
            raise exception
        else:
            self.load_template_details(template)
            return True

    def load_template_details(self, details):
        self.name = details[0]["Template_Name"]
        self.id = details[0]["Template_Id"]
        self.varaint_list = []
        for d in details:
            self.varaint_list.append(Variant(d["Variant_Id"], variant_name=d["Variant_VariantName"], html_body=d["Variant_HTML"], subject=d["Variant_Subject"]))

    def to_json(self):
        return self.__dict__

