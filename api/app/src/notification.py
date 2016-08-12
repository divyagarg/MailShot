from app.src.contactinfo import ContactInfo
from app.src.mailtrack import MailTrack

__author__ = 'divyagarg'


def bounce(message_id, bounce_obj):
    bounce_type = bounce_obj.get('bounceType')
    bounce_subtype = bounce_obj.get('bounceSubType')
    bounced_recipients = bounce_obj.get('bouncedRecipients')
    for recipent in bounced_recipients:
        # Marking contact as Invalid
        contact = ContactInfo(email = recipent.get('emailAddress'))
        contact.mark_contact_invalid(bounce_type, bounce_subtype)
        # Marking email as bounce for given message id
        mailtrack = MailTrack(message_id = message_id)
        return mailtrack.update_bounce_status()


def complaint(message_id):
    # Marking the mail as Spam
    mailtrack = MailTrack(message_id= message_id)
    return mailtrack.mark_email_as_spam()


def delivery(message_id):
    # Marking the email as Delivered
    mailtrack = MailTrack(message_id = message_id)
    return mailtrack.mark_email_as_delivered()

def process_notification(args):
    message = args.get('Message')
    notification_type = message.get('notificationType')
    message_id = args.get('MessageId')
    if notification_type == 'Bounce':
        return bounce(message_id, message.get('bounce'))
    elif notification_type == 'Complaint':
        return complaint(message_id)
    elif notification_type == 'Delivery':
        return delivery(message_id)
