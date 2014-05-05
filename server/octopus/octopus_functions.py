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
	print "============"	
	d = {}
	d = json.dumps(data)
	
	db.nodes.update({'_id':data['_id']},data,upsert=True)
	return "cadastrado"

def insert_logs_crud(data):
	db = con_db()
	db.logs.insert(data)
	return "salvo"

def remove_crud():
	print "remove"

def retrieve_nodes_crud():
	db = con_db()
	nodes = db.nodes.find()
	return nodes

def retrieve_logs_crud():
	db = con_db()
	logs = db.logs.find()
	return logs

def retrieve_crud(data,campo):
	try:
		db = con_db()
		s = db.nodes.find_one({'_id':data})
		print "[+] Campo: "+campo
		print "[+] resultado: ",s[campo]
		return s[campo]
	except Exception, e:
		print "[!] Falhou!"
		print e
# EOF - CRUD

#x02 - RN
def comandos(com):	
	print "==============="
	print com
	print "==============="
	maquina = com['node']
	comando = com['command']+" "+com['params']

	print "[+] servidor: "+maquina
	print "[+] comando: "+comando
	res = retrieve_crud(maquina,"ip")
	print "[-] IP: ",res
	thread.start_new_thread(envia_comando,(res,comando))	
	return {'retorno':'enviado'}
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
