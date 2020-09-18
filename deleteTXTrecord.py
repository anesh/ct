import requests
import json
import re
requests.packages.urllib3.disable_warnings() 


sep = "/"
user = ''
pwd = ''



f1 = open('fqdns.txt','r')
refobjs = f1.readlines() 


req_params = {'view': 'Internal' }

for refobj in refobjs:
        column=refobj.split()
        fqdn= str(column[0])
        url = "https://ibgrid/wapi/v2.7/record:txt?name~="+fqdn
        response = requests.request("GET", url, params=req_params, auth=(user,pwd),verify=False)
        values= response.text
        print values
        jsonv = json.loads(values)
        try: 
		x = jsonv[0]['_ref']
	except:
    		continue
	y = x.split(sep,1)[1]
        refid = y.split(":")[0]
        print refid



	url = "https://ibgrid/wapi/v2.7/record:txt/"+refid



	payload = json.dumps(values) 
	headers = {'content-type': "application/json"}
	response = requests.request("DELETE", url, auth=(user,pwd), headers=headers,verify=False)
	print response.text

