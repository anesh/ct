import os
import paramiko
import socket
import re
import sys
import time
from ciscoconfparse import CiscoConfParse
import getpass
import json


filename=sys.argv[1]


f1 = open(filename,'r')
devices = f1.readlines()


username = ""
password =  ""


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


for device in devices:
    column = device.split()
    try:
	ssh.connect(column[0], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show running-config ')
	config = stdout.readlines()
	parse = CiscoConfParse(config)
	#iphelper=parse.find_objects("^ip dhcp relay address 10.126.4.100")
	iphelpers=parse.find_objects_w_child(parentspec=r"^interface", childspec=r"ip dhcp relay address")
	for iphelper in iphelpers:
		print iphelper.text
		for child in iphelper.children:
			print child.text
	'''
	if iphelper:
		print column[0]+ "  Completed"
	if not iphelper:
		print column[0]+ "  "
	'''
    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)		 
        

		
    
	
