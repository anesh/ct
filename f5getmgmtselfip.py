import bigsuds
import os
import xlsxwriter


f1 = open('f5devices.txt', 'r')

devices = f1.readlines()

book = xlsxwriter.Workbook('/tmp/f5_mgmt_self_ips.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Device","Management IP Address","Self-IPs"]
for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)
row=0


for device in devices:
	row=row+1
    	column = device.split()
	print column[0]
        sheet.write(row,0,column[0])

	try:

		b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
		device = b.Management.Device.get_local_device()
                mgmtip = b.Management.Device.get_management_address([device])
                for ip in mgmtip:
                        sheet.write(row,1,ip)

		selfiplist=b.Networking.SelfIPV2.get_list()
		output=b.Networking.SelfIPV2.get_address(selfiplist)
		for out in output:
			row=row+1
			sheet.write(row,2,out)
	except bigsuds.ConnectionError:
		try:
			b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
			device = b.Management.Device.get_local_device()
	                mgmtip = b.Management.Device.get_management_address([device])
        	        for ip in mgmtip:
                	        sheet.write(row,1,ip)

                	selfiplist=b.Networking.SelfIPV2.get_list()
                	output=b.Networking.SelfIPV2.get_address(selfiplist)
                	for out in output:
                        	row=row+1
                        	sheet.write(row,2,out)

		except bigsuds.ConnectionError:
			try:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				device = b.Management.Device.get_local_device()
	                        mgmtip = b.Management.Device.get_management_address([device])
        	                for ip in mgmtip:
                	                sheet.write(row,1,ip)

                        	selfiplist=b.Networking.SelfIPV2.get_list()
                        	output=b.Networking.SelfIPV2.get_address(selfiplist)
                        	for out in output:
                                	row=row+1
                                	sheet.write(row,2,out)

			except bigsuds.ConnectionError:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				device = b.Management.Device.get_local_device()
                                mgmtip = b.Management.Device.get_management_address([device])
                                for ip in mgmtip:
                                        sheet.write(row,1,ip)

                                selfiplist=b.Networking.SelfIPV2.get_list()
                                output=b.Networking.SelfIPV2.get_address(selfiplist)
                                for out in output:
                                        row=row+1
                                        sheet.write(row,2,out)

				

f1.close()
book.close()
