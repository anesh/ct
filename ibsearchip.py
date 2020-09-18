import requests
import xlsxwriter
import json
requests.packages.urllib3.disable_warnings() 
import re
import sys

def main():
	f1 = open('ltmips.txt','r')

	book = xlsxwriter.Workbook('/tmp/f5__core_dnsV2.xlsx')
	sheet = book.add_worksheet("report")

	header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
	header = ["LTM Virtual Address","External FQDN","Internal FQDN","External CNAME","Internal CNAME"]
	for col, text in enumerate(header):
        	sheet.write(0, col, text, header_format)

	row=0

	ips = f1.readlines()
	for ip in ips:
    		row=row+1
    		column = ip.split()
    		print column[0]
		sheet.write(row,0,column[0])

		internallist = []
		externallist = []
		#ADD AD USERNAME AND PASSWORD HERE	
		user = ""
        	pwd = ""

		req_params = {'view': 'External' }
		url = "https:///wapi/v2.7/record:a?ipv4addr="+str(column[0])
		response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
		values= response.text
		jsonv = json.loads(values)
	
		print "######### FQDNS External #########\n"
		for j in jsonv:
        		x = j['name']
			print x
			externallist.append(x)
        	
		req_params = {'view': 'Internal' }
        	url = "https:///wapi/v2.7/record:a?ipv4addr="+str(column[0])
        	response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        	values= response.text
        	jsonv = json.loads(values)

        	print "######## FQDNS Internal ###########\n"
        	for j in jsonv:
                	x = j['name']
                	print x
			internallist.append(x)

		req_params = {'view': 'External' }
		print "######### CNAME External #########\n"
		for external in  externallist:
			row=row+1
			sheet.write(row,1,external)
        		url = "https:///wapi/v2.7/record:cname?canonical="+external
        		response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        		values= response.text
        		jsonv = json.loads(values)

        		for j in jsonv:
        			x = j['name']
                		print x
				sheet.write(row,3,x)

        	req_params = {'view': 'Internal' }
		print "######## CNAME Internal ###########\n"
		for internal in internallist:
			row=row+1
			sheet.write(row,2,internal)
        		url = "https:///wapi/v2.7/record:cname?canonical="+internal
        		response = requests.request("GET", url,params=req_params, auth=(user,pwd),verify=False)
        		values= response.text
        		jsonv = json.loads(values)
			
        		for j in jsonv:
				row=row+1
                		x = j['name']
				print x
				sheet.write(row,4,x)
	
	book.close()
	f1.close()
	

if __name__ == '__main__':
    main()
