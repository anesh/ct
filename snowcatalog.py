import requests
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
from bs4 import BeautifulSoup

url = 'https://cantire.service-now.com/api/sn_sc/servicecatalog/items/f407edc14fd082007b3c926ca310c7c7/order_now'
headers = {"Content-Type":"application/json","Accept":"application/json"}

user = ''
pwd = ''
adshortid = ''
startdate = '2019,08,19'
enddate = '2019,08,23'
cardid = '240044 309236 11101474324-1'

getuserurl='https://cantire.service-now.com/api/now/table/sys_user?sysparm_query=user_name='+adshortid
xmlheader = {"Accept":"application/xml"}
userresponse = requests.get(getuserurl, auth=(user, pwd), headers=xmlheader)
soup = BeautifulSoup(userresponse.text,'xml')
titles = soup.find_all('sys_id')
for title in titles:
    uname = title.get_text()
    
s = startdate.split(',')
e = enddate.split(',')

a = date(int(s[0]),int(s[1]),int(s[2]))
b = date(int(e[0]),int(e[1]),int(e[2]))

for dt in rrule(DAILY, dtstart=a, until=b):
    dateval= dt.strftime("%Y-%m-%d")


    params = { 'sysparm_quantity': '1','variables': {'manager_dcar':'6d0c3be04f6a1200ec6600fe9310c7a3','requested_for':uname,'type_dcar':'Employee','swipe_card_id_dcar': cardid,
		'start_date_dcar': dateval+' 08:00:00','end_date_dcar': dateval+' 18:00:00','reason_dcar':'Project','ITSR_Project_ID_dcar':'Network Core Refresh',
                'access_location_dcar':'2e2c099a4facc200070300fe9310c791','comments_dcar':'various Network initiatives'}}
    payload = json.dumps(params)
    response = requests.post(url, auth=(user, pwd), headers=headers, data=payload)

    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    data = response.json()
    print(data)
