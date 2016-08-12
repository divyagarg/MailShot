import logging
from flask import g
from app.src.sqlalchemydb import AlchemyDB

logger = logging.getLogger()
__author__ = 'divyagarg'


class ContactInfo(object):

    def __init__(self, contactId = None, email=None, name = None, age =None, gender=None, isValid = True, subscriptionStatus = 1, reason = None):
        self.contactId = contactId
        self.email = email
        self.name = name
        self.age = age
        self.gender = gender
        self.isValid = isValid
        self.subscriptionStatus = subscriptionStatus
        self.reason = reason

    def getContact(self):
        logger.debug("%s Getting contact detail for given Contact id  %s", g.UUID, self.contactId)
        db = AlchemyDB()
        try:
            contactInfo = db.find_one(table_name="ContactInfo", ContactId = self.contactId)
        except Exception as exception:
            logger.error("in exception")
            raise exception
        else:
            self.load_contact_info(contactInfo)
            return True

    @staticmethod
    def find_contact_by_email(email):
        db = AlchemyDB()
        try:
            contactInfo = db.find_one(table_name="ContactInfo", Email=email)
        except Exception as exception:
            raise exception
        else:
            if contactInfo:
                contact = ContactInfo()
                contact.load_contact_info(contactInfo)
                return contact
            return False

    def load_contact_info(self, contactInfo):
        self.email = contactInfo.get('Email')
        self.name = contactInfo.get('Name')
        self.age = contactInfo.get('Age')
        self.gender =contactInfo.get('Gender')
        self.isValid = contactInfo.get('IsValid')
        self.subscriptionStatus = contactInfo.get('SubscriptionStatus')
        self.reason = contactInfo.get('Reason')

    def mark_contact_invalid(self, bounce_type, reason):
        db = AlchemyDB()
        try:
            contactInfo = db.find_one(table_name="ContactInfo", Email = self.email)

            self.contactId = contactInfo.get('ContactId')
            where = {'ContactId': self.contactId}
            val = {'IsValid' : 2 if bounce_type == 'Permanent' else 3, 'Reason': reason}
            result = db.update_row_new("ContactInfo", where=where, val=val)
        except Exception as exception:
            logger.error(exception)
            raise exception
        return result