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
# x01 - CRUD
# x02 - RN
# x03 - Sockets
#

import socket
import json
from pymongo import *
import thread
import time
import os

# --- configuration --- #
host = ''
port = 7000
# ----------------------#


#x01---- CRUD - MongoDb -----
def con_db():
	client = MongoClient('localhost',27017)
	db = client["octopus"]
	return db

def insert_crud(data):
	print "inserindo: ",data
	db = con_db()	
	d = {"_id":data['_id']}
	db.servers.update(d,data,True)
	

def remove_crud():
	print "remove"

def retrieve_servers_crud(data):
	db = con_db()
	servers = db.servers.find()
	return servers

def retrieve_crud(data,campo):
	try:
		db = con_db()
		s = db.servers.find_one({'_id':data})
		print "[+] Campo: "+campo
		print "[+] resultado: ",s
		return s[campo]
	except Exception, e:
		print "[!] Falhou!"
		print e
# EOF - CRUD

#x02 - RN
def comandos(com):
	#path = "scripts/"
	#commands = next(os.walk("scripts/"))[2]
	#if "scripts" in com:
	#	print commands
	maquina = com.split(" ")[0].strip()
	comando = com.split(" ",1)[1]

	print "[+] servidor: "+maquina
	print "[+] comando: "+comando
	res = retrieve_crud(maquina,"ip")
	print "[-] IP: ",res
	envia_comando(res,comando)
#EOF -- RN --

#x03 -- Sockets ----
def cria_socket(ip):
	try:
		addr = ((ip,port))
		agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		agent_socket.connect(addr)
		print "[+] conectou no ip: ",ip		
		return agent_socket
	except Exception,e:
		print e

def envia_comando(ip,com):
		print "[+] Enviando comando"
		try:
			s = cria_socket(ip)
			s.send(com)
		except Exception, e:
			print "[!] Falhou!"
			print e
#EOF -- Sockets --		

#nada
def retorno_dict():
	d = {"cabelo":"dedo"}
	return d

#thread.start_new_thread(comandos,(comando,))
