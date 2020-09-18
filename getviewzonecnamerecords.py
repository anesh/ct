import requests
import json
requests.packages.urllib3.disable_warnings() 

user = ''
pwd = ''

querystring = {"_max_results":"10","_paging":"1","_return_as_object":"1"}

url = "https:///wapi/v2.7/zone_auth?view=External&_return_as_object=1"
response = requests.request("GET", url, auth=(user,pwd),params=querystring,verify=False)
next_page_id = response.json()['next_page_id']

while next_page_id:
        query = {"_page_id":next_page_id}
        newresponse = requests.request("GET", url, auth=(user,pwd),params=query,verify=False)
        values= newresponse.text
        jsonv = json.loads(values)
        for val in jsonv['result']:
                        zoneval = val['fqdn']
			recordsurl = "https:///wapi/v2.7/record:cname?zone="+zoneval+"&view=External&_return_as_object=1"
			try:
				recordsesponse = requests.request("GET", recordsurl, auth=(user,pwd),verify=False)
				recordsval = recordsesponse.text
				#print recordsval
				jsonrecords = json.loads(recordsval)
        			for records in jsonrecords['result']:
                        		cnameval = records['canonical']
					nameval = records['name']
					print cnameval,nameval
			except Exception:
				continue

	try:
                next_page_id = newresponse.json()['next_page_id']
        except Exception:
		next_page_id = 0
