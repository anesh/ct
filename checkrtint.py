import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import logging
logging.getLogger('paramiko.transport').setLevel(logging.DEBUG)
paramiko.util.log_to_file("example.log")   

#username = raw_input('Enter username for device login:')
#password =  getpass.getpass()

f1 = open('subnet1.txt','r')

book = xlsxwriter.Workbook('routecheck.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Route","Results","Ouptut"]
for col, text in enumerate(header):
        sheet.write(0, col, text, header_format)



devices = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
row=0

for device in devices:
    row=row+1
    column = device.split()
    print column[0]
    try:
    	ssh.connect('', username="", password="",timeout=5,allow_agent=False,look_for_keys=False)
        remote_conn = ssh.invoke_shell()
	output = remote_conn.recv(1000)
	print output
	remote_conn.send('show ip route vrf all | i ' +column[0]+'\n')
        output = remote_conn.recv(1000)
	print output
	'''
	rtoutput=stdout.readlines()
	if not rtoutput:
		print "Route Not Found"
		sheet.write(row,0,column[0])
		sheet.write(row,1,"Route Not Found")
	else:
		for rt in rtoutput:
			print rt
                        sheet.write(row,0,column[0])
                        sheet.write(row,1,"Route Found")
                        sheet.write(row,2,rt)
	'''
                                                                                  

    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)

book.close()
f1.close()









 
