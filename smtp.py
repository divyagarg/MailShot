__author__ = 'divyagarg'
import boto.ses

conn = boto.ses.connect_to_region('eu-west-1',
								  aws_access_key_id= 'AKIAI2ZNLE7EET4LHENQ',
								  aws_secret_access_key='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')

conn.send_email(
        'divya.garg@askme.in',
        'Test Email: Mark it spam',
        'Hello!! Welcome to AskMe. ',
        ['divya.garg@askme.in', 'ruchi@askme.in'])




