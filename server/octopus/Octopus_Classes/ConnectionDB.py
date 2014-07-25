#!/usr/bin/python

from pymongo import *

class ConnectionDB:
	
	def ConnectionDB(self):
		client = MongoClient('localhost',27017)
		db = client["octopus"]
		return db
