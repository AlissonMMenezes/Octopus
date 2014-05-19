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


import os
import time
import subprocess
import urllib2
import json
import thread
import re
from time import *
import platform
import socket
import binascii
import sys


#webservice module
from cornice import Service
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from pyramid.response import Response

#Variaveis de configuracao
con = None
config = {}

def _create_token():
	return binascii.b2a_hex(os.urandom(20))

def valid_token(request):
	header = 'X-Octopus-Token'
	token = request.headers.get(header)
	if token is None:
		raise _401()
	token = token.split('-')
	if len(token) != 2:
		raise _401()
	user, token = token
	valid = user in _USERS and _USERS and _USERS[user] == token
	if not valid:
		raise _401()
	request.validated['user'] = user

def read_config_file():
	if os.stat('octopus.config')[6] == 0:
		print '[!] Arquivo de configuracao vazio'
		exit()
	f = open('octopus.config','r+')
	for line in f:
		if '=' in line:
			atrib = line.split('=')[0].strip()
			config[atrib] = line.split('=')[1].strip()
	if 'token' not in config.keys():
		config['token'] = _create_token()
		f.write("token = "+config['token'])
		cadastra_agent()
		
	f.close()

def get_agent_config():
	ps = ""
	if "Windows" in platform.platform():
		ps = r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe"
		ip = subprocess.Popen([ps,"ipconfig | findstr IPv4 | %{$_.split(':')[1]}"],stdout=subprocess.PIPE,shell=True).communicate()[0]
	else:
		ip = subprocess.Popen(["ifconfig eth0| grep 'inet end' | awk '{print $3}'"],stdout=subprocess.PIPE,shell=True).communicate()[0]
		m = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
		if not m.match(ip):
			ip = subprocess.Popen(["ifconfig eth0| grep 'inet addr:' | cut -f 2 -d : | awk '{print $1}'"],stdout=subprocess.PIPE,shell=True).communicate()[0]
	agent_config = { "_id":"default",
				 "nodes":{
				 	"hostname":socket.gethostname(),
				 	"ip":ip,
				 	"token":config['token']
				 	}
				}
	return agent_config


def cadastra_agent():	
	try:
		jsun = json.dumps(get_agent_config())
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
		ret = subprocess.Popen([ps,data],stdout=subprocess.PIPE,shell=True).communicate()[0]
		print "[-] Saida do comando: ",ret
		hora = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		d = {"data":hora, "node":agent_config['nodes']['hostname'],"comando":l[0],"args":l[1],"output":ret}
		j = json.dumps(d)
		#envia json para output
		print "[-] Enviando output"
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




#
#
# Services
#
#
comando = Service(name='comando', path='/comando', description='Roda os comandos no S.O.')
@comando.get()
def get_comando(request):
	print "====== REQUEST ========"
	print request
	#run_command(request.body)
	return {"retorno":"ok"}


def main():
	print "[!] Iniciando agent!"
	config = Configurator()
	config.include("cornice")
	config.scan()  
	app = config.make_wsgi_app()
	print "[+] Aguardando instrucoes"
	server = make_server('0.0.0.0', 7000, app)
	server.serve_forever()


if __name__ == '__main__':
	read_config_file()	
	main()