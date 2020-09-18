import requests
import json
requests.packages.urllib3.disable_warnings()
import sqlite3
conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
c.execute('''CREATE TABLE virtualpolicyobjs (vname text,vpolicy text)''')


user = ""
pwd = ""
poollist =[]
url = "https:///mgmt/tm/ltm/virtual/?expandSubcollections=true"
response = requests.request("GET", url,auth=(user,pwd),verify=False)
values= response.text
parsed = json.loads(values)
#print json.dumps(parsed,indent=4, sort_keys=True)
for jsonout in parsed['items']:
	try:
		print jsonout['name'],jsonout['partition']
		virtualname = jsonout['name']
		for d in jsonout['policiesReference']['items']:
			print d['name']
			vpolicyname = d['name']
			c.execute('INSERT INTO virtualpolicyobjs VALUES (?,?)',(virtualname,vpolicyname))
	except Exception as e:
		print e

conn.commit()
conn.close()


