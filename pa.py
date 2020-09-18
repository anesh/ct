import requests
import argparse
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import os
import xlsxwriter
import re


f1 = open('pa.txt','r')

book = xlsxwriter.Workbook('pa.xlsx')



interfaces=[]
loginterfaces=[]
devices = f1.readlines()
for device in devices:
	row=0
        connfail = ""
        column = device.split()
        ip=column[1]
        print column[0]

	sheet = book.add_worksheet(column[0])
	header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
	header = ["IP address","Interface Name","Zone","Tag","VSYS","Virtual Router"]
	for col, text in enumerate(header):
        	sheet.write(0, col, text, header_format)

	try:
		#rest api call for api key
  		r = requests.get('https://'+ip+'/api/?type=keygen&user=username&password=password',verify=False, timeout=5)
		markup = r.text
		soup = BeautifulSoup(markup, "xml")
		key = soup.find_all('key')
		api=key[0].get_text()


		#rest call for system information
		r = requests.get('https://'+ip+'/api/?type=op&cmd=<show><system><info></info></system></show>&key='+api,verify=False,timeout=5)
		tags =r.text
		infomarkup = BeautifulSoup(tags, "xml")

		#rest call for hardware interface information
		r = requests.get('https://'+ip+'/api/?type=op&cmd=<show><interface>hardware</interface></show>&key='+api,verify=False, timeout=5)
		hwinttags=r.text
		hwintmarkup=BeautifulSoup(hwinttags, "xml")

		#rest call for logical interface information
		r = requests.get('https://'+ip+'/api/?type=op&cmd=<show><interface>logical</interface></show>&key='+api,verify=False, timeout=5)

		loginttags=r.text
		logintmarkup=BeautifulSoup(loginttags, "xml")
	except requests.exceptions.Timeout:
		print "Connection Timedout"
		connfail = "Connection Timedout"
		sheet.write(row,0,"Connection Timedout")
	'''
	for interface in hwintmarkup.find_all("entry"):
        	interfaced={'name':str(interface.find('name').get_text()),
                    	    'duplex':str(interface.duplex.get_text()),
                            'state':str(interface.state.get_text()),
                            'mac':str(interface.mac.get_text()),
                                }
        	interfaces.append(interfaced)

	for interface in interfaces:
		print interface
	'''
	if connfail != "Connection Timedout":
		for logint in logintmarkup.find_all("entry"):
			print logint
        		logintd={'name':str(logint.find('name').get_text()),
                        	 'zone':str(logint.zone.get_text()),
                         	'ip':str(logint.ip.get_text()),
				'tag':str(logint.tag.get_text()),
				'vsys':str(logint.vsys.get_text()),
				'vr':str(logint.fwd.get_text())
                         	}	
        		loginterfaces.append(logintd)

		for loginterface in loginterfaces:
			row=row+1
			print loginterface
			sheet.write(row,0,loginterface['ip'])
			sheet.write(row,1,loginterface['name'])
			sheet.write(row,2,loginterface['zone'])
			sheet.write(row,3,loginterface['tag'])
			sheet.write(row,4,loginterface['vsys'])
			sheet.write(row,5,loginterface['vr'])
book.close()
f1.close()

