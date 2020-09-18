import requests
import json
requests.packages.urllib3.disable_warnings() 


f1 = open('att.txt','r')

attributes = f1.read().splitlines() 

citylist=[]

for att in attributes:
     citylist.append({'value': att})


newdict={"list_values": citylist}
url = "https://ib/wapi/v2.7/extensibleattributedef/b25lLmV4dGVuc2libGVfYXR0cmlidXRlc19kZWYkLlN0cmVldF9BZGRyZXNz:Street_Address"
payload = json.dumps(newdict) 
headers = {'content-type': "application/json"}
response = requests.request("PUT", url, auth=('', ''), data=payload, headers=headers,verify=False)
print response.text
