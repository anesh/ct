import bigsuds
import requests
import json
requests.packages.urllib3.disable_warnings()
import sqlite3
conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
c.execute('''CREATE TABLE policyobjs (policyname text,policypool text,policypoolmember text)''')


user = ""
pwd = ""
poollist =[]
b = bigsuds.BIGIP(hostname = "",username = user, password = pwd)
url = "https:///mgmt/tm/ltm/policy/?expandSubcollections=true"
response = requests.request("GET", url,auth=(user,pwd),verify=False)
values= response.text
parsed = json.loads(values)
for itemsdict in parsed['items']:
	try:
		pcyname = itemsdict['name']
		print itemsdict['name'], itemsdict['partition']
		
		for actions in itemsdict['rulesReference']['items']:
			#print json.dumps(actions['actionsReference']['items'][0],indent=4, sort_keys=True)
			x=actions['actionsReference']['items'][0]
			for key,value in x.iteritems():
				if key == "pool":
					print key,value
					pname = value
					poolmembers = b.LocalLB.Pool.get_member_v2([pname])
					for poolmember in poolmembers:
						for addressport in poolmember:
							addport = str(addressport['address'])+":"+str(addressport['port'])
							print addport
							c.execute('INSERT INTO policyobjs VALUES (?,?,?)',(pcyname,pname,addport))	
	except Exception, e:
		print e

conn.commit()
conn.close()



