from threading import Thread
from Queue import Queue
import requests
requests.packages.urllib3.disable_warnings()
import json


concurrent = 500

def doWork():
    while True:
	ip = q.get()
	try:
		print ip
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
                #d[subnet] = prefix
        except Exception as e:
                print e
                pass

        q.task_done()


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('delta1.txt'):
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
