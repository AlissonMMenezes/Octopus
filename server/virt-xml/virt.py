#!/usr/bin/python

import libvirt
import pprint

c = libvirt.open("qemu:///system")
Vms = c.listAllDomains()
for v in Vms:
	pprint.pprint(dir(v))
	print v._conn

