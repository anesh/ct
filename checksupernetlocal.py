from netaddr import *  
import json

prefixlist = []
privateprefixlist =[]

with open('test2.json') as f:
    data = json.load(f)
    for prefixes in data ['TABLE_vrf']['ROW_vrf']['TABLE_addrf']['ROW_addrf']['TABLE_prefix']['ROW_prefix']:
	prefixlist.append(prefixes['ipprefix'])


#Removing default route
prefixlist.pop(0)



with open('delta.txt','r') as f:
    deltaips = [i for i in f]


for deltaip in deltaips:
    for ipnetwork in prefixlist:
        if IPAddress(deltaip) in IPNetwork(ipnetwork):
                if IPAddress(deltaip).is_private():
                        print ipnetwork



