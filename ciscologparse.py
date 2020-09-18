import os
import paramiko
import socket
import re
import sys
import time
from ciscoconfparse import CiscoConfParse
import getpass
import json


f1 = open('dev.txt','r')
devices = f1.readlines()


username = raw_input('Enter username for device login:')
password =  getpass.getpass()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


for device in devices:
    column = device.split()
    try:
	ssh.connect(column[0], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show running-config ')
	config = stdout.readlines()
	parse = CiscoConfParse(config)
	loghost1=parse.find_objects("^logging host ")
	loghost2=parse.find_objects("^logging host ")
	loghost3=parse.find_objects("^logging host ")
	loghost4=parse.find_objects("^logging host ")
	trap=parse.find_objects("^logging trap debugging")
	originid=parse.find_objects("^logging origin-id hostname")
	timedebug=parse.find_objects("^service timestamps debug datetime msec localtime show-timezone")
	timelog=parse.find_objects("^service timestamps log datetime msec localtime show-timezone year")

	if loghost1 and loghost2 and loghost3 and loghost4 and trap and originid and timedebug and timelog:
		print column[0]+ "  Completed"
	if not loghost1:
		print column[0]+ "  loghost1 not ok"
	if not loghost2:
		print column[0]+ "  loghost2 not ok"
	if not loghost3:
		print column[0]+ "  loghost3 not ok"
	if not loghost4:
		print column[0]+ "  loghost4 not ok"
	if not trap:
		print column[0]+ "  trap not ok"
	if not originid:
		print column[0]+ "  originid not ok"
	if not timedebug:
		print column[0]+ "  timedebug not ok"
	if not timelog:
		print column[0]+ "  timelog not ok"

    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)		 
        

		
    
	
