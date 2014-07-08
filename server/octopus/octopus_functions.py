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
import pymongo
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
	print "Recebido: ",data
	db = con_db()		
	nodes = db.nodes.aggregate([
			    {"$project":{ "_id":1,"nodes.ip":1,"nodes.hostname":1,"nodes.feet":1}},
			    { "$unwind":"$nodes" },
			    { "$match":{"_id":data["_id"]}}
			]);
	print "============================"
	print data['nodes']['ip']
	for f in nodes['result']:
		print f['nodes']['ip']
	print "============================"

	if len(nodes['result']) <= 0:
		print "Nenhum agent cadastrado"
		db.nodes.update({"_id":data["_id"]},{"$addToSet":{"nodes":data["nodes"]}},upsert=True)
		return "Cadastrando agent!!!"
	else:
		e = 0
		print "Entrou aqui"
		for f in nodes['result']:
			print "ips: ",f['nodes']['ip']
			if data['nodes']['ip'] in f['nodes']['ip']:
				print "Existe"
				db.nodes.update({"_id":data['_id'],"nodes.ip":data['nodes']['ip']},{"$set":{"nodes.$":data['nodes']}})
				retorno = "Atualizando agent"
				e = 1
				break
			else:
				print "Nao existe"
				retorno = "Novo agent"
		if e != 1:
			db.nodes.update({"_id":data["_id"]},{"$addToSet":{"nodes":data["nodes"]}},upsert=True)
		return retorno
		

def insert_grupo_crud(data):
	db = con_db()	
	j = { "_id":data["_id"], "feet":[],"nodes":[]}
	db.nodes.insert(j)
	return {"retorno":"cadastrado"}

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

def delete_group_crud(data):
	if data['_id'] == 'default':
		return {"retorno":"O Grupo default nao pode ser excluido"}
		
	db = con_db()
	nodes = db.nodes.aggregate([
			    {"$project":{ "_id":1,"nodes.ip":1,"nodes.hostname":1}},
			    { "$unwind":"$nodes" },
			    { "$match":data}
			]);
	print "#########################"
	print nodes["result"]
	for i in nodes['result']:
		print "incluindo ",i['nodes']," para o grupo default!"
		db.nodes.update({"_id":"default"},
					{"$addToSet":{"nodes":i['nodes']}}
					,upsert=True)
	rem = db.nodes.remove(data)
	
	return {"retorno":"Grupo excluido"}

def retrieve_logs_crud():
	db = con_db()
	logs = db.logs.find().sort("data",pymongo.DESCENDING).limit(20)
	return logs

def retrieve_feet_crud():
	db = con_db()
	feet = db.feet.find()
	return feet

def find_foot_crud(data):
	db = con_db()
	feet = db.feet.find_one(data)
	return feet

def add_foot_crud(data):
	db = con_db()
	r = db.feet.update({"_id":data['_id']},data,upsert=True)
	return {"retorno":"cadastrado com sucesso!"}

def delete_foot_crud(data):
	db = con_db()
	feet = db.feet.remove(data)
	return {"retorno":"removido"}

def add_foot_to_node(data):
	db = con_db()
	db.nodes.update({"_id":data['grupo'],"nodes.hostname":data['hostname']},
					{"$addToSet":{"nodes.$.feet":data['foot']}}
					,upsert=True)
	return {"retorno":"Adicionado!"}

def add_foot_to_group(data):
	db = con_db()
	db.nodes.update({"_id":data['grupo']},
					{"$addToSet":{"feet":data['foot']}}
					,upsert=True)
	return {"retorno":"Adicionado!"}

def remove_foot_from_group(data):
	db = con_db()
	db.nodes.update({"_id":data['grupo']},
					{"$addToSet":{"feet":data['foot']}}
					,upsert=True)
	return {"retorno":"Adicionado!"}


def retrieve_crud(data,campo):
	try:
		db = con_db()
		#s = db.nodes.find_one({'_id':data})
		s = db.nodes.aggregate([
			    {"$project":{ "_id":0,"nodes.ip":1,"nodes.hostname":1}},
			    { "$unwind":"$nodes" },
			    { "$match":{"nodes.hostname":data}}
			]);
		res = s["result"][0]["nodes"][campo]		
		print "[+] Campo: "+campo
		print "[+] resultado: ",res
		return res
	except Exception, e:
		print "[!] Falhou!"
		print e

def retrieve_node_info(data):
	try:
		print "================"
		print data
		db = con_db()
		#s = db.nodes.find_one({'_id':data})
		s = db.nodes.aggregate([
			    {"$project":{ "_id":1,"feet":1,"nodes.ip":1,"nodes.hostname":1,"nodes.feet":1}},
			    { "$unwind":"$nodes" },
			    { "$match":{"nodes.hostname":data['hostname']}}
			]);
		res = s["result"][0]
		print "[+] resultado: ",res
		return res
	except Exception, e:
		print "[!] Falhou!"
		print e
# EOF - CRUD

#x02 - RN
def comandos(com):	
	res = []
	print "==============="
	print com
	print "==============="
	maquinas = com['nodes']
	comando = com['command']+" "+com['params']
	print "========= MAQUINAS ======"
	print maquinas
	try:
		for m in maquinas:
			print "[+] servidor: "+m
			res.append(retrieve_crud(m,"ip"))
		print "[+] comando: "+comando	
		for i in res:
			print "[-] IP: ",i
			thread.start_new_thread(envia_comando,(i,comando))	
		
		return {'retorno':'enviado'}
	except Exception, e:
		print "[!] Erro!"
		print e
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