import logging

from app.errors import MailShotException
from app.src import ERROR_STATUS_CODE
from app.src.sqlalchemydb import AlchemyDB
from flask import g
from sqlalchemy.exc import IntegrityError

__author__ = 'divyagarg'

logger = logging.getLogger()

class Template(object):

	def __init__(self, name, userid):
		self.name = name
		self.userid =userid
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
			logger.error(exception, exc_info = True)
			db.rollback()
			raise exception
		else:
			db.commit()
			return True
		return False


class Variant(object):

	def __init__(self, variant_name, html_body, template_id, subject):
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
			args = {"VariantName": self.variant_name, "HTML": self.html_body, "TemplateId": self.template_id, "Subject": self.subject}
			self.id = db.insert_row("Variant", **args)
			logger.debug(self.id)
		except IntegrityError as err:
			logger.error('%s Template Id %s do not exist', g.UUID, self.template_id, err, exc_info=True)
			raise MailShotException(err, ERROR_STATUS_CODE.TEMPLATE_ID_DO_NO_EXIST)
		except Exception as exception:
			logger.error(exception, exc_info = True)
			db.rollback()
			raise exception
		else:
			db.commit()
			return True
		return False

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
			logger.error(exception, exc_info = True)
			db.rollback()
			raise exception
		else:
			return segments
