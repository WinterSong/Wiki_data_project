# coding: utf-8
import MySQLdb
import json

class querys:
	"""docstring for querys"""
	def __init__(self):
		self.conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='test',port=3306)
		self.cur = self.conn.cursor()

	def final(self):
		self.cur.close()
		self.conn.close()

	# def getProperty(self,localId,pid):
	# 	print localId, pid
	# 	print '='*20
	# 	self.cur.execute('select datatype, datavalue_value, property from snaks where localId=%s and property=%s',[localId,pid])
	# 	tmpJson = self.cur.fetchall()[0]
	# 	datatype = tmpJson[0]
	# 	data = tmpJson[1]
	# 	propertyId = tmpJson[2]
	# 	print datatype
	# 	print '='*20
	# 	self.cur.execute('select labels_en_value from property where id=%s',[propertyId])
	# 	pName = self.cur.fetchall()[0]
	# 	if datatype == 'wikibase-item':
	# 		objId = json.loads(data)['id']		
	# 		self.cur.execute('select labels_en_value from item where id=%s',[objId])
	# 		objName=self.cur.fetchall()[0]
	# 		return (pName,objName,objId)
	# 	elif datatype in 'string':
	# 		return (pName, json.loads(data),'none')
	# 	# elif datatype == 'time':
	# 	else:
	# 		return (pName,data,'none')


	def query1(self,name):
		# select entities whose name is just "name"
		self.cur.execute('select id from aliases where value=%s',[name])
		ids = [i[0] for i in self.cur.fetchall()]
		dsc = []
		for ide in ids:
			self.cur.execute('select descriptions_en_value from item where id=%s',[ide])
			dsc+=self.cur.fetchall()
		dsc = [i[0] for i in dsc]
		return ids,dsc

	def query2(self,id):
		self.cur.execute('select datavalue_value from snaks where item_id=%s and property=\"P31\"',[id])
		instanceOf = self.cur.fetchall()
		instanceOf = [i[0] for i in instanceOf]
		temp = {}
		for iof in instanceOf:
			obj_id = json.loads(iof)['id']
			self.cur.execute('select labels_en_value from item where id=%s',[obj_id])
			temp[obj_id] = self.cur.fetchall()[0][0]
		self.cur.execute('select datavalue_value from snaks where item_id=%s and property=\"P279\"',[id])
		subclassOf = [i[0] for i in self.cur.fetchall()]
		for iof in subclassOf:
			obj_id = json.loads(iof)['id']
			self.cur.execute('select labels_en_value from item where id=%s',[obj_id])
			temp[obj_id] = self.cur.fetchall()[0][0]
		return temp


	def getProperty(self,dataType,dataValue):
		if dataType=='string':
			return ('string',json.loads(dataValue))
		elif dataType == 'wikibase-entityid':
			objId = json.loads(dataValue)['id']
			self.cur.execute('select labels_en_value from item where id=%s',[objId])
			objName = self.cur.fetchall()[0][0]
			return ('entity',objId,objName)
		elif dataType == 'globecoordinate':
			obj = json.loads(dataValue)
			latitude = obj['latitude']
			longitude= obj['longitude']
			out = ''
			if latitude:
				if latitude<0:
					out += str(-1*latitude)+'°S'
				else:
					out += str(latitude)+'°N'
			out+=','
			if longitude:
				if longitude<0:
					out += str(-1*longitude)+'°E'
				else:
					out += str(longitude)+'°W'
			return ('location',out)
		elif dataType == 'monolingualtext':
			obj = json.loads(dataValue)
			return ('text',obj['text']+'('+obj['language']+')')
		elif dataType == 'time':
			obj = json.loads(dataValue)
			time = obj['time'].split('T')[0]
			out = ''
			if time[0] == '-':
				out = 'BCE '
			time = time[1:]
			out += time
			return ('time',out)
		elif dataType == 'quantity':
			obj = json.loads(dataValue)
			amount = obj['amount']
			if amount[0] == '+':
				amount = amount[1:]
			unit = obj['unit']
			if unit =='1':
				return ('quantity',amount)
			unit = unit.split('/')[-1]
			self.cur.execute('select labels_en_value from item where id=%s',[unit])
			unitName = self.cur.fetchall()[0][0]
			try:
				return ('quantity',amount+unitName)
			except:
				return ('quantity', amount)

		else:
			return ('others',dataValue)


	def matchProperty(self, outlineProperty, allProperty):
		# match[property||localId] = content
		match = {}
		result = {}
		for propertyTuple in allProperty:
			match[propertyTuple[2]+'||'+propertyTuple[3]] = self.getProperty(propertyTuple[0],propertyTuple[1])
		for propertyTuple in outlineProperty:
			self.cur.execute('select labels_en_value from property where id=%s',[propertyTuple[0]])
			propertyName = self.cur.fetchall()[0][0]
			if propertyName not in result:
				result[propertyName] = []
			tmpResult = {}
			tmpResult['property'] = match[propertyTuple[0]+'||'+propertyTuple[3]]
			if propertyTuple[1] != None:
				self.cur.execute('select labels_en_value from property where id=%s',[propertyTuple[1]])
				qualifierName = self.cur.fetchall()[0][0]
				tmpResult['qualifier'] = match[propertyTuple[1]+'||'+propertyTuple[3]]
				tmpResult['qualifierName'] = qualifierName
			else:
				tmpResult['qualifier'] = (None,None)
			if propertyTuple[2] != None:
				self.cur.execute('select labels_en_value from property where id=%s',[propertyTuple[2]])
				referenceName = self.cur.fetchall()[0][0]
				tmpResult['reference'] = match[propertyTuple[2]+'||'+propertyTuple[3]]
				tmpResult['referenceName'] = referenceName
			else:
				tmpResult['reference'] = (None,None)
			result[propertyName].append(tmpResult)
		return result




	def query4(self,id):
 		# all properties and statement an entity possesses 

 		# get the basic information of this entity
 		self.cur.execute('select labels_en_value,descriptions_en_value from item where id=%s',[id])
 		out = self.cur.fetchall()[0]
 		info = {}
 		info['name'] = out[0]
 		info['description'] = out[1]

 		# get all aliases of an entity
		self.cur.execute('select value from aliases where id=%s',[id])
		aliases = [i[0] for i in self.cur.fetchall()]

		# get the outline of the statement
		self.cur.execute('select property, qualifier_property, references_property, id from claims where id like %s',[id+'$%'])
		outlineProperty = self.cur.fetchall()

		# get all properties from snaks of the item
		self.cur.execute('select datavalue_type, datavalue_value, property, localId from snaks where item_id=%s',[id])
		allProperty = self.cur.fetchall()

		result = self.matchProperty(outlineProperty,allProperty)
		return info,aliases,result

	def query5(self,query):
		# given item name and property description, output list of tuple in form of 
		# (property,qualifier,reference)
		from parse import parseQP
		qids, propertyName = parseQP(query)
		out = []
		for qid in qids:
			info,aliases,result = self.query4(qid)
			if propertyName not in result:
				continue
			out.append((info,aliases,{propertyName:result[propertyName]}))
		return out[0]

if __name__ == '__main__':
	qry = querys()
	print qry.query5('population of New York City')