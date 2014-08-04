#!/usr/bin/python

import libvirt

try:
	c = libvirt.open("qemu+ssh://root@localhost/system")	
	print c.getHostname()
	pool = con.define_
	c.createXML('teste.xml')
except Exception, e:
	print 'Erro!!! ',e


