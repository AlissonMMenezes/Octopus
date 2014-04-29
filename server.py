#!/usr/bin/python
#
# Octopus - IT Automation Tool
# Coded by: Alisson Menezes
#		- alisson.copyleft@gmail.com
#		
# Date: 29/04/2014
#
# Central Configuration Server
#	
#

import socket
import json
import pymongo

# --- configuration --- #
host = ''
port = 7000
max_host = 10000
# ----------------------#

# Managing agents

agents = {}

addr = (host, port)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
serv_socket.bind(addr)
serv_socket.listen(max_host)

print '[!] aguardando conexoes'
while True:
	con, con1 = serv_socket.accept()
	recebe = con.recv(1024)
	if recebe.startswith('connected:'):
		print recebe



print recebe
