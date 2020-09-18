import re
import csv
import requests
requests.packages.urllib3.disable_warnings()
#from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Pool
import json

d ={}
def do_work(subnet):
	try:
		global count
		count = count + 1
		print count
		ip = subnet.strip("\n")
		command = "show ip route "+ip+" vrf core"
		url = "https:///ins"
		user = ''
		pwd = ''
        	rvalues =   {"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": command ,"output_format": "json"}}
        	rpayload = json.dumps(rvalues)
		headers = {'content-type': "application/json"}
		rresponse = requests.post(url, data=rpayload, headers=headers,auth=(user,pwd), verify=False)
    		print rresponse.request.headers
		print rresponse.status_code
		if rresponse.status_code == 401:
                        cookie = ""

		data = json.loads(rresponse.text)
		prefix= data ['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']['TABLE_addrf']['ROW_addrf']['TABLE_prefix']['ROW_prefix']['ipprefix']
		print prefix
		d[subnet] = prefix
	except Exception as e:
                print e
		pass
	


def writetoexcel():
	with open('out1.csv', 'wb') as outfile:
    		writer = csv.writer(outfile)
    		# to get tabs use csv.writer(outfile, dialect='excel-tab')
    		writer.writerows(d.iteritems())



if __name__ == '__main__':
	f1 = open('delta1.txt','r')
	subnets = f1.readlines()
	count = 0
	pool = Pool(processes=100)
	#pool = ThreadPool(1000)	
    	pool.map(do_work, subnets)
	writetoexcel()





 
