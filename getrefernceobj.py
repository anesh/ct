import requests
import json
requests.packages.urllib3.disable_warnings() 
import re
from bs4 import BeautifulSoup
import urlparse

sep = "/"
user = ''
pwd = ''


f1 = open('fqdns.txt','r')

refobjs = f1.readlines()

req_params = {'view': 'Internal' }

dval = {}

for refobj in refobjs:
	column=refobj.split()
	fqdn= str(column[0])
	url = "https://ibgrid/wapi/v2.7/record:txt?name~="+fqdn
	response = requests.request("GET", url, params=req_params, auth=(user,pwd),verify=False)
	values= response.text
	print values
	jsonv = json.loads(values)
	x = jsonv[0]['_ref']
	z= jsonv[0]['text']
	zt = z[:-1]
	dt=urlparse.parse_qs(zt)
	sv= dt['site'][0]
     	ltv=dt['locationtype'][0]
	sbv= dt['sbu'][0]
	pv =dt['pci'][0]
	dv= dt['device'][0]
	mv =dt['model'][0]
	zv = dt['zone'][0]
	lv = dt['location'][0]
	print sv,ltv,sbv,pv,dv,mv,zv,lv
	y = x.split(sep,1)[1]
	refid = y.split(":")[0]
	#print refid
