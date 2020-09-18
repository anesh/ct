import requests
import json
requests.packages.urllib3.disable_warnings() 
import re
from bs4 import BeautifulSoup
import urlparse

sep = "/"
user = ''
pwd = ''

querystring = {"_max_results":"5","_paging":"1","_return_as_object":"1"}

url = "https:///wapi/v2.7/record:a?zone=ns.ctc&view=Internal"
response = requests.request("GET", url, auth=(user,pwd),params=querystring,verify=False)
values= response.text
print values
	
jsonv = json.loads(values)
#print jsonv['result'][0]
for val in jsonv['result']:
	print val['name']+" "+val['ipv4addr']
