import bigsuds
import sqlite3
conn = sqlite3.connect('vipstatus.db')
c = conn.cursor()
c.execute('''CREATE TABLE vipstatus (vname text,vavail text,venabled text,vdesc text,vip text,ip text)''')



device=raw_input('Enter Device :')

outputFile = open('virtualswdc.txt', 'w+')
b = bigsuds.BIGIP(hostname = device,username = '', password = '',)
partlist=b.Management.Partition.get_partition_list()
for part in partlist:
  pname= part['partition_name']
  partcount=len(partlist) 
  print >>outputFile,"*****"+pname+"****" 
  b.Management.Partition.set_active_partition(pname)
  virtuals=b.LocalLB.VirtualServer.get_list()
  for virtual in virtuals:
	status=b.LocalLB.VirtualServer.get_object_status([virtual])
	destination =  b.LocalLB.VirtualServer.get_destination([virtual])
	print virtual, status[0]['availability_status'],status[0]['enabled_status'],status[0]['status_description']
	avail=status[0]['availability_status']
        enab = status[0]['enabled_status']
        desc = status[0]['status_description']
	vip = str(destination[0]['address'])+":"+str(destination[0]['port'])
	ip =  str(destination[0]['address'])
	print ip
	c.execute('INSERT INTO vipstatus VALUES (?,?,?,?,?,?)',(virtual,avail,enab,desc,vip,ip))

conn.commit()
conn.close()
