import requests
import json
requests.packages.urllib3.disable_warnings() 

user = ''
pwd = ''

querystring = {"_max_results":"10","_paging":"1","_return_as_object":"1"}

url = "https://ibgrid/wapi/v2.7/zone_auth?view=External&_return_as_object=1"
response = requests.request("GET", url, auth=(user,pwd),params=querystring,verify=False)
next_page_id = response.json()['next_page_id']

while next_page_id:
        query = {"_page_id":next_page_id}
        #query = {"_return_fields":"extattrs,name,ipv4addrs"}
        newresponse = requests.request("GET", url, auth=(user,pwd),params=query,verify=False)
        values= newresponse.text
        jsonv = json.loads(values)
        for val in jsonv['result']:
                        zoneval = val['fqdn']
			recordsurl = "https://ibgrid/wapi/v2.7/record:a?zone="+zoneval+"&view=External&_return_as_object=1"
			try:
				recordsesponse = requests.request("GET", recordsurl, auth=(user,pwd),verify=False)
				#print zoneval
				recordsval = recordsesponse.text
				jsonrecords = json.loads(recordsval)
        			for records in jsonrecords['result']:
                        		nameval = records['name']
					recordsipv4= records['ipv4addr']
					print nameval,recordsipv4
			except Exception:
				continue

	try:
                next_page_id = newresponse.json()['next_page_id']
        except Exception:
		next_page_id = 0
