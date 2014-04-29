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
import thread
import time

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

def comandos(com):
	commands = {'list_hosts',"get_info","help"}
	if "list_hosts" in com:
		print agents.keys()
	elif "get_info" in com:
		print "oi"
	elif com == "help":
		print commands
	elif "disconnect" in com:		
		hn = com.split(" ")[1]
		agents[hn].send("disconnect")

def conexoes(lol):
	print '[!] aguardando conexoes'
	while True:
		try:
			con, con1 = serv_socket.accept()
			recebe = con.recv(1024)
			if recebe.startswith('[!] connected'):
				hn = recebe.split('-')[1].strip().split(':')[0]
				agents[hn] = con
				print "[!] "+hn+" conectado"
		except Exception,e:
			print "[!] Erro: ",e



	print recebe


try:
	thread.start_new_thread(conexoes,('',))
except Exception, e:
	print '[!] Erro: ',e
while True:
	comando = raw_input('>> ')
	comandos(comando)
