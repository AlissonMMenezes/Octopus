#!/usr/bin/python

import ConnectionDB

class LogsDAO:
	def save(self, node):
		try:
			db = ConnectionDB.ConnectDB()
			db.logs.insert(node)
			return {"retorno":"Salvo"}
		except Exception, e:
			return {"erro":e}

	def delete(self, node):
		db = ConnectionDB.ConnectionDB()
		db.logs.insert(node)


	def search(self, id):
		db = ConnectionDB()
		db.logs.find_one({"id":id})

	def update(self, id, node):
		con = ConnectionDB()
		db.logs.insert(node)

	def all_logs(self):
		try:
			db = ConnectionDB.ConnectionDB()
			l = db.logs.find()
			return l
		except Exception, e:
			print "EXCEPTION: ",e