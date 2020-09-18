import requests
import json
import csv
requests.packages.urllib3.disable_warnings() 

user = ''
pwd = ''

ipurl= "https://ibgrid/wapi/v2.7/ipv4address"

with open('ho.csv') as csvfile:
	extvals = csv.DictReader(csvfile)
	for row in extvals:
		#print row['IP_Address']
		ipval = row['IP_Address']
		extquery = {"_return_fields":"network","ip_address":ipval}
		try:
			extresponse = requests.request("GET", ipurl, auth=(user,pwd), params=extquery,verify=False)

			extvalues= extresponse.text
			#print extvalues
			extjson = json.loads(extvalues)
			netval = extjson[0]['network']
			print ipval,netval
		except KeyError:
                        print "No Network Found for "+ipval
                        continue




