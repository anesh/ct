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

for prefix in prefixlist:
	print prefix
