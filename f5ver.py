import bigsuds
import os
import base64
import threading





f1 = open('f5devices3.txt', 'r')

devices = f1.readlines()

for device in devices:
    	column = device.split()
	try:

		b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
		ver=b.System.SystemInfo.get_version()
		print column[0]+","+column[1]+","+ver
	except bigsuds.ConnectionError:
		try:
			b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
			ver=b.System.SystemInfo.get_version()
			print column[0]+","+column[1]+","+ver
			
		except bigsuds.ConnectionError:
			try:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
                		ver=b.System.SystemInfo.get_version()
				print column[0]+","+column[1]+","+ver
			except bigsuds.ConnectionError:
				b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
                                ver=b.System.SystemInfo.get_version()
				print column[0]+","+column[1]+","+ver

			



f1.close()
