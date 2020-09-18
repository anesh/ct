import json
import netaddr
import time


ipset1 = netaddr.IPSet(open('ciscosubnets.txt','r').readlines())
ipset2 = netaddr.IPSet(open('nexposesubnets.txt','r').readlines())

print "Set 1:", len(ipset1), "IP addresses"
print "Set 2:", len(ipset2), "IP addresses"

start = time.time()
ipset = ipset2 - ipset1

for cidr in ipset.iter_cidrs():
	if cidr.is_private():
		print cidr
