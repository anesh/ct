import requests
import json
import re
requests.packages.urllib3.disable_warnings() 


f1 = open('nodeids.txt','r')

nodeids = f1.readlines() 


for vals in nodeids:
	column= vals.split()
	nodeid= str(column[0])
	print nodeid

	url = "https://p5cbeasolra02.internal.ctfs.com:17778/SolarWinds/InformationService/v3/Json/swis://p5cbeasolra02.internal.ctfs.com/Orion/Cli.DeviceTemplatesNodes/NodeId="+nodeid
	print url
	values = { "TemplateId":-1,"NodeId":nodeid }
	print values

	payload = json.dumps(values) 
	headers = {'content-type': "application/json",'Content-Length': "29"}
	response = requests.request("POST", url, auth=('ctfs\\aneke', 'Tantra@chakki1'), data=payload, headers=headers,verify=False)
	print response.status_code

