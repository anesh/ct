import re
import csv
import requests
requests.packages.urllib3.disable_warnings()
import json
import time

d ={}
cookie = "" 
count = 0
f1 = open('delta.txt','r')
subnets = f1.readlines()
url = ""
user = ''
pwd = ''



for subnet in subnets:
	try:
		count = count +1
		print count
		ip = subnet.strip("\n")
		command = "show ip route "+ip+" vrf core"
        	rvalues =   {"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": command ,"output_format": "json"}}
        	rpayload = json.dumps(rvalues)
		headers = {'content-type': "application/json"}
		if not cookie:
			values =   {"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": "show ip route" ,"output_format": "json"}}
			payload = json.dumps(values)
                	headers = {'content-type': "application/json"}
			response = requests.post(url,data=payload, headers=headers,auth=(user,pwd), verify=False)
			print response.status_code
			print response.headers
			cookie = requests.utils.dict_from_cookiejar(response.cookies)
			print "fisrt auth cookie\n"
			print cookie	
		rresponse = requests.post(url, data=rpayload, headers=headers,cookies=cookie, verify=False)
		print rresponse.request.headers
		print rresponse.status_code
		if rresponse.status_code == 401:
			cookie = ""
		print rresponse.headers
		print rresponse.cookies
		data = json.loads(rresponse.text)
		prefix= data ['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_addrf']['ROW_addrf']['TABLE_prefix']['ROW_prefix']['ipprefix']
		print prefix
		d[subnet] = prefix
	except Exception as e:
                print e
		continue

	


with open('out.csv', 'wb') as outfile:
	writer = csv.writer(outfile)
    		# to get tabs use csv.writer(outfile, dialect='excel-tab')
	writer.writerows(d.iteritems())








 
