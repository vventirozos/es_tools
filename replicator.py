#!/usr/bin/python
import json
import pprint
import select
import psycopg2
import psycopg2.extensions
import requests
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

try:
	conn = psycopg2.connect("dbname='monkey' user='postgres' host='127.0.0.1' password='noneed'")
except:
	print "I am unable to connect to the database"

conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN table_messages_notifier;")

print "Waiting for notifications on channel 'table_messages_notifier'"
while True:
        if select.select([conn],[],[],5) == ([],[],[]):
                pass
        else:
                conn.poll()
	while conn.notifies:
		notify = conn.notifies.pop()
		print "Got new record with id: ", notify.payload
                my_id=notify.payload
                cur = conn.cursor()
                cur.execute("""select * from messages where id="""+ my_id )
                (id, date, carrier, message) = cur.fetchone()[:4]
                doc = {
                'id': id,
                'date': date,
                'carrier': carrier,
                'message': message
                } 
                res = es.index(index="messages", doc_type='messages', id=my_id, body=doc)
#                row = cur.fetchone()
#                print row
#		res = es.index(index="vasilis", doc_type='my_test', id=my_id, body=row)


#                my_id=notify.payload
#                url='http://localhost:9200/_river/my_data/'+my_id
#                payload = {"type": "jdbc", "jdbc": {"url": 'jdbc:postgresql://localhost:5432/monkey', 'user': 'postgres', 'password' :'','sql': 'select * from test where id=%s' % my_id}}
#                headers = {'content-type': 'application/json'}
#		print payload
#		r = requests.put(url, data=json.dumps(payload))
#		print(r.url)
#		print r.text


#, notify.pid, notify.channel, notify.payload
#	print notify.payload
#
#cur = conn.cursor()
#cur.execute("""SELECT * from test;""")
#rows = cur.fetchall()
#my_name = "Vasilis"
#print "\nShow me the records:\n"
#for row in rows:
#        print row
#
