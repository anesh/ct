import bigsuds
import os
import xlsxwriter


f1 = open('f5devices.txt', 'r')

devices = f1.readlines()

book = xlsxwriter.Workbook('/tmp/f5_system_info.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Device","TMOS Version","chassis_serial","host_board_serial","Registration Keys"]
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
		ver=b.Management.Device.get_version()
		sheet.write(row,1,ver)
		sysinfo=b.System.SystemInfo.get_system_information()
		sheet.write(row,2,sysinfo['chassis_serial'])
		sheet.write(row,3,sysinfo['host_board_serial'])
		regkeys=b.Management.LicenseAdministration.get_registration_keys()
		sheet.write(row,4,regkeys[0])
	except bigsuds.ConnectionError:
		try:
			b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
			ver=b.Management.Device.get_version()
	                sheet.write(row,1,ver)
        	        sysinfo=b.System.SystemInfo.get_system_information()
                	sheet.write(row,2,sysinfo['chassis_serial'])
         	       	sheet.write(row,3,sysinfo['host_board_serial'])
               		regkeys=b.Management.LicenseAdministration.get_registration_keys()
                	sheet.write(row,4,regkeys[0])

		except bigsuds.ConnectionError:
			try:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				ver=b.Management.Device.get_version()
		                sheet.write(row,1,ver)
                		sysinfo=b.System.SystemInfo.get_system_information()
               			sheet.write(row,2,sysinfo['chassis_serial'])
              			sheet.write(row,3,sysinfo['host_board_serial'])
                		regkeys=b.Management.LicenseAdministration.get_registration_keys()
                		sheet.write(row,4,regkeys[0])

			except bigsuds.ConnectionError:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				ver=b.Management.Device.get_version()
		                sheet.write(row,1,ver)
               			sysinfo=b.System.SystemInfo.get_system_information()
                		sheet.write(row,2,sysinfo['chassis_serial'])
                		sheet.write(row,3,sysinfo['host_board_serial'])
               			regkeys=b.Management.LicenseAdministration.get_registration_keys()
                		sheet.write(row,4,regkeys[0])

				

f1.close()
book.close()
