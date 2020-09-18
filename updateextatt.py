import requests
import json
import re
import urlparse
requests.packages.urllib3.disable_warnings()


sep = "/"
user = ''
pwd = ''



f1 = open('fqdns.txt','r')
refobjs = f1.readlines()


req_params = {'view': 'Internal' }

for refobj in refobjs:
        column=refobj.split()
        fqdn= str(column[0])
        url = "https://ib/wapi/v2.7/record:txt?name~="+fqdn
        response = requests.request("GET", url, params=req_params, auth=(user,pwd),verify=False)
        values= response.text
        print values
        jsonv = json.loads(values)
        try:
                x = jsonv[0]['_ref']
        except:
                continue
        y = x.split(sep,1)[1]
        refid = y.split(":")[0]
	z= jsonv[0]['text']
        zt = z[:-1]
        dt=urlparse.parse_qs(zt)
        sv= dt['site'][0]
        ltv=dt['locationtype'][0]
        sbv= dt['sbu'][0]
        pv =dt['pci'][0]
        dv= dt['device'][0]
        mv =dt['model'][0]
        zv = dt['zone'][0]
        lv = dt['location'][0]


        url = "https://10.2.61.100/wapi/v2.7/record:txt/"+refid


	values = {"extattrs": {"site": { "value": sv },
                              "locationtype": { "value": ltv },
			      "sbu": { "value": sbv },
                              "pci": { "value": pv },
			      "device": { "value": dv },
                              "model": { "value": mv },
                              "zone": { "value": zv },
			      "location": { "value": lv }}} 

        payload = json.dumps(values)
        headers = {'content-type': "application/json"}
        response = requests.request("PUT", url, auth=(user,pwd), data=payload, headers=headers,verify=False)
        print response.text

