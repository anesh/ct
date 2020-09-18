import requests
import json
import re
import urlparse
requests.packages.urllib3.disable_warnings()


user = ''
pwd = ''



f1 = open('fqdns.txt','r')
refobjs = f1.readlines()


req_params = {'view': 'Internal' }

for refobj in refobjs:
        column=refobj.split()
        fqdn= str(column[0])
        url = "https:///wapi/v2.7/record:host?name~="+fqdn
        response = requests.request("GET", url, params=req_params, auth=(user,pwd),verify=False)
        values= response.text
        #print values
        jsonv = json.loads(values)
        x = jsonv[0]['_ref']
	#print x
	extupdateurl= "https:///wapi/v2.7/"+x
	values = {"extattrs": {"device": { "value": "yes" }}}

	payload = json.dumps(values)
        headers = {'content-type': "application/json"}
        response = requests.request("PUT",extupdateurl, auth=(user,pwd), data=payload, headers=headers,verify=False)
        print response.text


