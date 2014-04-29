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
import os

#Variaveis de configuracao
config = {'server':'','port':''}

if os.stat('octopus.config')[6] == 0:
	print '[!] Arquivo de configuracao vazio'
	exit()

f = open('octopus.config','r')


for line in f:
	if '=' in line:
		atrib = line.split('=')[0].strip()
		config[atrib] = line.split('=')[1].strip()

addr = ((config['server'],int(config['port'])))
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent_socket.connect(addr)

agent_socket.send("connected: ["+socket.gethostname()+"]")
