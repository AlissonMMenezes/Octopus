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
import time
import subprocess
import urllib2
import json
import thread
import re
from time import *

ip = subprocess.Popen(["ifconfig eth0| grep 'inet end' | awk '{print $3}'"],stdout=subprocess.PIPE,shell=True).communicate()[0]
m = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
if not m.match(ip):
	ip = subprocess.Popen(["ifconfig eth0| grep 'inet addr:' | cut -f 2 -d : | awk '{print $1}'"],stdout=subprocess.PIPE,shell=True).communicate()[0]

#Variaveis de configuracao
con = None
max_host = 10000
config = {'server':'','port':''}
agent_config = { '_id':socket.gethostname(),
				  'ip':ip,
				  'group':'default'
				}

jsun = json.dumps(agent_config)
if os.stat('octopus.config')[6] == 0:
	print '[!] Arquivo de configuracao vazio'
	exit()

f = open('octopus.config','r')


for line in f:
	if '=' in line:
		atrib = line.split('=')[0].strip()
		config[atrib] = line.split('=')[1].strip()

def cadastra_agent(jsun):
	try:
		header = {"Content-Type":"application/json; charset=utf-8"}
		req = urllib2.Request('http://'+config['server']+":8080/cadastrar",jsun,header)
		handle = urllib2.urlopen(req)
		res = str(handle.read())
		if res == "cadastrado":
			print "[+] Agent cadastrado no servidor"
		else:
			print "[!] Erro ao cadastrar agent"
	except Exception, e:
		print "[!] Ocorreu um erro!"
		print e

def run_command(data):
	try:
		print "[-] Rodando comando: "+data		
		l = data.split(" ",1)
		print "============="
		print l
		ret = subprocess.Popen(l,stdout=subprocess.PIPE,shell=True).communicate()[0]
		print "[-] Saida do comando: ",ret
		hora = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		d = {"data":hora, "node":agent_config['_id'],"comando":l[0],"args":l[1],"output":ret}
		j = json.dumps(d)

		#envia json para output
		print "[-] Enviando retorno"
		header = {"Content-Type":"application/json; charset=utf-8"}
		req = urllib2.Request('http://'+config['server']+":8080/output",j,header)
		handle = urllib2.urlopen(req)
		res = str(handle.read())
		if res == "salvo":
			print "[+] Logs cadastrados"
		else:
			print "[!] Logs nao cadastrados"
	except Exception, e:
		print "[!] Ocorreu um erro!"
		print e


def criaServidor():
	try:
		addr = ('', 7000)
		serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		serv_socket.bind(addr)
		serv_socket.listen(max_host)
		return serv_socket
	except Exception,e:
		print e




cadastra_agent(jsun)

s = criaServidor()
print "[+] Aguardando Conexao"
con, saddr = s.accept()

while True:
	print "[+] Aguardando instrucoes"
	recebe = con.recv(1024)
	thread.start_new_thread(run_command,(recebe,))
	if con == None or not con.recv(1024):
		print "[!] Servidor quebrou!\n[!] Tentando recriar..."
		try:
			recebe = None
			s = criaServidor()
			con, saddr = s.accept()
		except Exception, e:
			print "[!] Falha ao criar servidor"
			print e
	


