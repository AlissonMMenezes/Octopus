#!/usr/bin/python

import ConnectionDB

class NodesDAO:

	def save(self, node):
		db = ConnectionDB.ConnectionDB()
		db.nodes.insert(node)

	def delete(self, node):
		print "code here..."

	def search(self, id):
		print "code here..."

	def update(self, id, node):
		print "code here..."

	def all_nodes(self):
		try:
			db = ConnectionDB.ConnectionDB()
			n = db.nodes.find()
			return n
		except Exception, e:
			return {"erro":e}
