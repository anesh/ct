import requests
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
from bs4 import BeautifulSoup

url = 'https://servicenow/api/now/table/cmdb_ci_ip_switch?sysparm_offset=40&sysparm_limit=2'
headers = {"Content-Type":"application/json","Accept":"application/json"}

user = ''
pwd = ''

#response = requests.get(url, auth=(user, pwd), headers=headers)
#print response.json()

params = { 'sysparm_quantity': '1','variables': {'dns_domain':'test1.ns.ctc','name':'test1','ip_address':'6.6.6.6'}}

payload = json.dumps(params)
response = requests.post(url, auth=(user, pwd), headers=headers, data=payload)

print response.text

if response.status_code != 200: 
	print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

data = response.json()
print(data)
