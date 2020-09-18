import bigsuds
import os
import datetime
import base64
import glob
import subprocess
import smtplib
from email.mime.text import MIMEText



f1 = open('/home1/ffolder/f5devices.txt', 'r')

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
	f = open('/tmp/' + filename + '.ucs', 'ab')
        try:

                b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
		print "try ctc ad pass"
		print "saving ucs for"+column[0]
        	b.System.ConfigSync.save_configuration(filename,"SAVE_FULL")

        except bigsuds.ConnectionError:
                try:
                        b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
			print "try ctb ad pass"
			print "saving ucs for"+column[0]
	
			b.System.ConfigSync.save_configuration(filename,"SAVE_FULL")

                except Exception as e:
			print e
                        try:
                                b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				print "try ctc local pass"
				print "saving ucs for"+column[0]
        			b.System.ConfigSync.save_configuration(filename,"SAVE_FULL")

                        except bigsuds.ConnectionError:
                                b = bigsuds.BIGIP(hostname = column[1],username = '', password = '')
				print "try ctb local pass"
				print "saving ucs for"+column[0]
        			b.System.ConfigSync.save_configuration(filename,"SAVE_FULL")




	print "downloading ucs for"+column[0]
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
	listoffiles=glob.glob("/tmp/*.ucs")
	print listoffiles
	for files in listoffiles:
        	#subprocess.Popen("curl --insecure --user root:Canyon+paint1 -T"+""+files+""+"scp://10.2.62.16/var/f5backups/",shell = True)
        	#subprocess.call(["curl","--insecure","--user",pwd,"-T"+files,"scp://10.2.62.16/var/f5backups/"])
        	subprocess.call(["sshpass","-v","-p",scppwd,"scp",files,"user@scpserver:/"])
        	subprocess.call(["rm","-f",files])

	

f1.close()



#Send mail

'''
with open('textfile', 'rb') as fp:
    msg = MIMEText(fp.read(),'html', 'utf-8')

recipients = ['']

msg['Subject'] = 'F5 UCS backup job completed'
msg['From'] = 'netdevops@cantire.com'
msg['To'] = ", ".join(recipients)

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('relay.cantire.com')
s.sendmail(msg['From'],recipients, msg.as_string())
s.quit()
'''
