#coding: utf-8
import MySQLdb

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='weiki',port=3306)
cur=conn.cursor()

#for i in range(1,11):
#	cur.execute('create table if not exists snaks{}(\
#		item_id varchar(20),\
#		datatype varchar(20),\
#		datavalue_type varchar(20),\
#		datavalue_value varchar(300),\
#		property varchar(20) not null,\
#		snaktype varchar(20),\
#		localId varchar(50),\
#		primary key (item_id,property,localId))'.format(i))


for id in range(1,10000000):
	tmpid = str(id)
	query = 'insert into snaks{} select * from snaks where item_id=\'P{}\' or item_id=\'Q{}\''.format(id%10+1,id,id)
	cur.execute(query)
cur.close()
conn.close()