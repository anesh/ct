import requests
import json
requests.packages.urllib3.disable_warnings() 
import re
from bs4 import BeautifulSoup
import urlparse

user = 'user'
pwd = 'pass'

def main(network):


	req_params = {'view': 'Internal' }

	dval = {}

	url = "https://ib_grid/wapi/v2.7/record:txt?name~="+fqdn+"&_return_fields=extattrs"
	response = requests.request("GET", url, params=req_params, auth=(user,pwd),verify=False)
	values= response.text
	jsonv = json.loads(values)
        z= jsonv[0]['extattrs']

	txtval = "site="+z['site']['value']+";"+"locationtype="+z['locationtype']['value']+";"+"sbu="+z['sbu']['value']+";"+"pci="+z['pci']['value']+";"+"device="+z['device']['value']+";"+"model="+z['model']['value']+"zone="+z['zone']['value']+";"+"location="+z['location']['value']
	print txtval

	url = "https://10.2.61.100/wapi/v2.7/record:txt"
	values = { "name":fqdn, "text":txtval,"view": "Internal" }


        payload = json.dumps(values)
        headers = {'content-type': "application/json"}
        response = requests.request("POST", url, auth=(user,pwd), data=payload, headers=headers,verify=False)
        print response.text

if __name__ == '__main__':
    main(network)

