#!/usr/bin/python
#
# Octopus - IT Automation Tool
# Arquivo que controla a LibVirt para criar maquinas virtuais
# Coded by: Alisson Menezes
#		- alisson.copyleft@gmail.com
#		
# Creation Date: 05/07/2014
#	
#

import libvirt
import xml.etree.ElementTree as ET
import os
import pprint
import uuid
import subprocess


def con_hypervisor():
	conn = libvirt.open("qemu+ssh://root@localhost/system")	
	print conn.getHostname()
	return conn

def get_Vms():
	c = con_hypervisor()
	Vms = c.listAllDomains()
	return Vms

def vm_action(data):
	action = data["action"]
	vm = data["vm"]
	print data
	#action, vm
	c = con_hypervisor()
	try:
		i = c.lookupByName(vm)
	except Exception, e:
		print "Falha ao buscar maquina virtual! ",e
	if action == "on":
		r = i.create()
	elif action == "off":
		r = i.shutdown()
	elif action == "pause":
		r = i.suspend()
	elif action == "resume":
		r = i.resume()
	elif action == "reboot":
		r = i.reboot()
	else:
		r = "desconhecido"
	print "=== Result ==="
	print r
	return {"retorno":r}

def access_console(data):
	c = con_hypervisor()
	vm = data["vm"]
	info = c.lookupByName(vm)
	xml = info.XMLDesc()
	with open(info.name()+".xml",'w') as f:
		for l in xml:
			f.write(l)
	f.close
	tree = ET.parse(info.name()+".xml")
	root = tree.getroot()
	for f in root.iter('graphics'):
		print f.attrib
		port = f.get('port')
	os.remove(info.name()+".xml")
	h = c.getHostname()
	return {"hostname":h,"port":port}

def get_networks(data):
	netw = {}
	l = []
	c = con_hypervisor()
	nets = c.listAllNetworks()
	pprint.pprint(dir(nets))
	for n in nets:
	 	f = open(n.name()+".xml",'w')
	 	f.write(n.XMLDesc())
	 	f.close()
	 	l.append(n.name())
	for i in l:
		tree = ET.parse(i+".xml")
		root = tree.getroot()
		for f in root.iter():
			netw[f.tag] = f.attrib, f.text
	return {"retorno":netw}

def create_vm(data):
	file = open("virt-xml/vm-template.xml",'r')
	texto = ''
	for f in file:
		texto += f
	file.close()
	mem = str((int(data['vm-mem'])*1024))
	texto = texto.replace('VM-NAME',data['vm-name']).replace('VM-CPU',data['vm-cpu']).replace('VM-MEM',mem)
	texto = texto.replace('VM-UID',str(uuid.uuid1())).replace('VM-ISO',data['vm-iso']).replace('VM-DISK',data['vm-name'])
	print texto
	
	if not os.path.isfile('/home/octopus/vms/'+data['vm-name']+'.xml'):
		try:
			file = open('/home/octopus/vms/'+data['vm-name']+'.xml','w+')
			file.write(texto)
			file.close
			print '[+] Arquivo xml criado!'					
			print data['vm-disk']
			ret = subprocess.Popen('qemu-img create -f raw  /home/octopus/vms/'+data['vm-name']+'.img '+data['vm-disk']+'G',stdout=subprocess.PIPE,shell=True).communicate()[0]
			print ret
			print '[+] Disco criado!'
			os.symlink('/home/octopus/vms/'+data['vm-name']+'.xml','/etc/libvirt/qemu/'+data['vm-name']+'.xml')	
		except Exception,e:
			print '[!] Erro! ',e
			os.remove('/home/octopus/vms/'+data['vm-name']+'.xml')
			retorno = "Erro!"
	else:
		retorno = 'A Maquina ja existe!'
		
	try:
			c = con_hypervisor()
			c.createXML(texto)
			retorno = "Maquina Criada!"
	except Exception, e:
		print e
		retorno = "Erro!!!"
	return {"retorno":retorno}

def get_iso(data):
	arqs = os.listdir('/home/octopus/ISO/')	
	return {"retorno":arqs}


#VM-NAME
#VM-CPU
#VM-MEM
#VM-UID
#VM-ISO
#VM-DISK
