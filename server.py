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
import os

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
	path = "scripts/"
	commands = next(os.walk("scripts/"))[2]
	if "scripts" in com:
		print commands
	elif "" in com:
		print "vazio"
	elif "get_info" in com:
		print "oi"
	elif "disconnect" in com:		
		hn = com.split(" ")[1]
		agents[hn].send("disconnect")
	elif "exit" in com:
		exit()
	else:
		print com
		f = open('scripts/'+com.split(" ")[0])
		hn = com.split(" ")[1]
		linha = f.readline()
		agents[hn].send("bash:"+linha)

def conexoes(lol):
	print '[!] aguardando conexoes'
	while True:
		try:
			con, caddr = serv_socket.accept()
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
