#!/usr/bin/python
#
# Octopus - IT Automation Tool
# Coded by: Alisson Menezes
#		- alisson.copyleft@gmail.com
#		
# Date: 29/04/2014
#
# 
# Octopus Agent	
#

import socket
import json
import os
import time

#Variaveis de configuracao
agent_socket = None
config = {'server':'','port':''}
agent_config = {
		'hostname':socket.gethostname(),
		'ip':socket.gethostbyname(socket.gethostname())

		}


if os.stat('octopus.config')[6] == 0:
	print '[!] Arquivo de configuracao vazio'
	exit()

f = open('octopus.config','r')


for line in f:
	if '=' in line:
		atrib = line.split('=')[0].strip()
		config[atrib] = line.split('=')[1].strip()

def criaSocket():
	try:
		addr = ((config['server'],int(config['port'])))
		agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		agent_socket.connect(addr)
		agent_socket.send("[!] connected - "+agent_config['hostname']+":"+agent_config['ip'])
		print "[+] Conectado\n[+] Aguardando Instrucoes"
		return agent_socket
	except Exception,e:
		print e


while True:
	if agent_socket == None or not agent_socket.recv(1024):
		agent_socket = None
		while agent_socket == None:
			print "[!] O servidor nao esta respondendo"
			time.sleep(5)
			agent_socket = criaSocket()

	try:
		recv = agent_socket.recv(1024)
		if "disconnect" in recv:
			print "[!] desativando o agent"
			exit()
		if recv.startswith("bash:"):
			c = recv.split(":")[1]
			os.system(c)
	except Exception, e:
		print "[!] Erro: ",e

