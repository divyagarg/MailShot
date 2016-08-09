import logging
from app.src.sqlalchemydb import AlchemyDB
from flask import g

__author__ = 'divyagarg'

logger = logging.getLogger()

class Variant(object):
    def __init__(self, variant_name=None, html_body=None, template_id=None, subject=None):
        self.variant_name = variant_name
        self.subject = subject
        self.html_body = html_body
        self.template_id = template_id
        self.id = None

    def save_variant(self):
        logger.debug("%s Insert_variant", g.UUID)
        db = AlchemyDB()
        db.begin()
        try:
            args = {"VariantName": self.variant_name, "HTML": self.html_body, "TemplateId": self.template_id,
                    "Subject": self.subject}
            self.id = db.insert_row("Variant", **args)
            logger.debug(self.id)
        # except IntegrityError as err:
        #     logger.error('%s Template Id %s do not exist', g.UUID, self.template_id, err, exc_info=True)
        #     raise MailShotException(err, ERROR_STATUS_CODE.TEMPLATE_ID_DO_NO_EXIST)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            db.rollback()
            raise exception
        else:
            db.commit()

        return self.id

    def to_json(self):
        return self.__dict__


