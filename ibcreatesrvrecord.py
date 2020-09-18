import requests
import json
requests.packages.urllib3.disable_warnings() 
import re
import sys


f1 = open('rdata_srv1.txt','r')




rdatas = f1.readlines()

for rdata in rdatas:
	user = ""
        pwd = ""
	rdatav = rdata.split()
	#rl = "https://10.2.61.100/wapi/v2.7/record:srv"
        values = { "name": rdatav[0], "port" : rdatav[6],"priority": rdatav[4],"target":rdatav[7],"view": "Internal", "weight":rdatav[5]}
        print values
	payload = json.dumps(values)
        headers = {'content-type': "application/json"}
        #response = requests.request("POST", url, data=payload, headers=headers, auth=(user,pwd),verify=False)
	print response.txt	
f1.close()
