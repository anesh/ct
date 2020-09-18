import bigsuds
import os
import datetime
import base64
import glob
import subprocess
import smtplib
from email.mime.text import MIMEText
from f5.bigip import ManagementRoot
import threading

def run_logcheck(logflag,filename):


    while logflag == 1:
	try:
		logs= b1.tm.util.bash.exec_cmd('run', utilCmdArgs='-c "grep '+filename+' /var/log/ltm"')
		result=logs.commandResult
		if result:
			logflag = 0
			print result
        		print("Stop polling.")
	except Exception as e:
		print "polling"



if __name__ == "__main__":

	f1 = open('f5devices3.txt', 'r')

	devices = f1.readlines()
	

	for device in devices:
		temp_date = str(datetime.datetime.utcnow())
	        split_date = str.split(temp_date)
        	my_date = split_date[0]
        	chunksize = 64*1024
        	file_offset = 0
        	flag =1

    	        column = device.split()
		filename = column[0]+ my_date
	        print "starting backup up of "+column[0]
        	f = open('/var/tmp/' + filename + '.ucs', 'ab')

        	try:
        		b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
			b1 = ManagementRoot(column[1], '', '')	
			print "saving ucs for"+column[0]
			b.System.ConfigSync.save_configuration(filename,"SAVE_FULL")

        	except Exception as e:
			print e
			logflag=1
			run_logcheck(logflag,filename)


		while flag == 1:
                        f5file=b.System.ConfigSync.download_configuration(filename + '.ucs',chunksize,file_offset)
                        #print f5file
                        f.write(base64.b64decode(f5file['return']['file_data']))
                        eof = f5file['return']['chain_type']
                        #print  eof
                        if eof == "FILE_LAST" or eof == "FILE_FIRST_AND_LAST":
                                flag = 0
                        file_offset = file_offset + chunksize
                        #print "Bytes Transferred:"+ str(file_offset)
                f.close()

                        #Delete ucs file from f5
                print "Deleting ucs file from f5 "+filename
                b.System.ConfigSync.delete_configuration(filename + '.ucs')

                #trasnfer files to BIGIQ and remove from automation server
                pwd=""
                scppwd=""
                listoffiles=glob.glob("/var/tmp/*.ucs")
                print listoffiles
                for files in listoffiles:
                        subprocess.call(["sshpass","-v","-p",scppwd,"scp",files,"user@scpserver:/"])
                        subprocess.call(["rm","-f",files])




	f1.close()

