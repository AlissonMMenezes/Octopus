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

#Variaveis de configuracao
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

try:
	print config
	addr = ((config['server'],int(config['port'])))
	agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	agent_socket.connect(addr)
except Exception,e:
	print e

agent_socket.send("[!] connected - "+agent_config['hostname']+":"+agent_config['ip'])
while True:
	print '[+] Aguardando'
	try:
		recv = agent_socket.recv(1024)
		if "disconnect" in recv:
			print "[!] desativando o agent"
			exit()
	except Exception, e:
		print "[!] Erro: ",e
