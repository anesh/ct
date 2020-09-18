import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import csv
from ciscoconfparse import CiscoConfParse
from multiprocessing.pool import ThreadPool

d ={}

def do_work(subnet):
    try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	ssh.connect('', username="", password="",timeout=5,allow_agent=False,look_for_keys=False)
        stdin,stdout,stderr = ssh.exec_command('show ip route '+subnet+' shorter-prefixes vrf core')
        rtoutput=stdout.readlines()
	print subnet
	rtentriesparse = CiscoConfParse(rtoutput)
        rtparams = rtentriesparse.find_objects("ubest/mbest")
	rtcount = len(rtparams)
	#for rt in rtparams:
	#	print rt.text
	if rtcount > 1:
		print "Route found"
		d[subnet] = "Route found"
	else:
		d[subnet] = "Route not found"
		print "Route not found"
                                                                                  
	ssh.close()
    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)


def writetoexcel():
	with open('out.csv', 'wb') as outfile:
    		writer = csv.writer(outfile)
    		# to get tabs use csv.writer(outfile, dialect='excel-tab')
    		writer.writerows(d.iteritems())



if __name__ == '__main__':
	f1 = open('subnet.txt','r')
	subnets = f1.readlines()
	pool = ThreadPool(28)	
    	print(pool.map(do_work, subnets))
	writetoexcel()





 
