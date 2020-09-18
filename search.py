import requests
import json
requests.packages.urllib3.disable_warnings() 
import re
import sys

def main():

	internallist = []
	externallist = []	
	user = ""
        pwd = ""
	req_params = {'view': 'External' }
	url = "https://ib/wapi/v2.7/record:a?ipv4addr="+str(sys.argv[1])
	#url = "https://10.2.61.100/wapi/v2.7/record:cname?canonical=woods.ca"
	response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
	values= response.text
	jsonv = json.loads(values)
	
	print "######### FODNS External #########\n"
	for j in jsonv:
        	x = j['name']
		print x
		externallist.append(x)
        	
	req_params = {'view': 'Internal' }
        url = "https://ib/wapi/v2.7/record:a?ipv4addr="+str(sys.argv[1])
        #url = "https://10.2.61.100/wapi/v2.7/record:cname?canonical=woods.ca"
        response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        values= response.text
        jsonv = json.loads(values)

        print "######## FODNS Internal ###########\n"
        for j in jsonv:
                x = j['name']
                print x
		internallist.append(x)

	req_params = {'view': 'External' }
	print "######### CNAME External #########\n"
	for external in  externallist:
        	url = "https://ib/wapi/v2.7/record:cname?canonical="+external
        	response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        	values= response.text
        	jsonv = json.loads(values)

        	for j in jsonv:
        		x = j['name']
                	print x

        req_params = {'view': 'Internal' }
	print "######## CNAME Internal ###########\n"
	for internal in internallist:
        	url = "https://ib/wapi/v2.7/record:cname?canonical="+internal
        	response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        	values= response.text
        	jsonv = json.loads(values)

        	for j in jsonv:
                	x = j['name']
                	print x
	
	

if __name__ == '__main__':
    main()
