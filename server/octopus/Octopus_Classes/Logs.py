#!/usr/bin/python

class Logs:	
	def __init__(self, patron_id, command, arguments, output, status):
		self.patron_id = patron_id
		self.command = command
		self.arguments = arguments
		self.output = output
		self.status = status
