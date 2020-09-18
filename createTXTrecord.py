import requests
import json
import re
requests.packages.urllib3.disable_warnings() 


f1 = open('fqdns.txt','r')

postvalues = f1.readlines() 


for postvalue in postvalues:
	postvalue
	column=postvalue.split()
	fqdn= str(column[0])
	txtval = re.findall(r'"([^"]*)"', postvalue)[0]
	print fqdn
	print txtval

	url = "https://ibgrid/wapi/v2.7/record:txt"

	values = { "name":fqdn, "text":txtval,"view": "Internal" }


	payload = json.dumps(values) 
	headers = {'content-type': "application/json"}
	response = requests.request("POST", url, auth=('', ''), data=payload, headers=headers,verify=False)
	print response.text

