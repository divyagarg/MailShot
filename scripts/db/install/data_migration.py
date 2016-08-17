import logging
import MySQLdb

mydb = MySQLdb.connect(host='127.0.0.1',
    user='root',
    db='MailShot')

# mydb = MySQLdb.connect(host='new-rds-askme.c0wj8qdslqom.ap-southeast-1.rds.amazonaws.com',
#     user='askme',
#     passwd='ma8ho2n3qdy9ew',
#     db='MailShot')
#
# mydb = MySQLdb.connect(host='orderengineproduction.c0wj8qdslqom.ap-southeast-1.rds.amazonaws.com',
#     user='OrderEngine',
#     passwd='OrderEngine1234',
#     db='MailShot')

logger = logging.getLogger()

def migrate_data():
    print "Starting Migration"
    cursor = mydb.cursor()

    with open('/Users/divyagarg/Downloads/Valid_Data_list_2.csv') as f:


        for line in f:
            line =  line.strip()
            print(line)
            try:
                sqlQuery =  "INSERT into ContactInfo (Email) value (\"" + line + "\")"
                cursor.execute(sqlQuery)
            except Exception as e:
                print(e)
            mydb.commit()
        cursor.close()
        print "Done"


migrate_data()