import bigsuds
import sqlite3
conn = sqlite3.connect('vipstatus.db')
c = conn.cursor()
f1 = open('fqdnvips.txt', 'r')
c.execute('''CREATE TABLE vipfqdn (vipfqdn text,ip text)''')


devices = f1.readlines()

for device in devices:
	column = device.split()
	fqdn = column[0]
	ip = column[1]
	print fqdn,ip
	c.execute('INSERT INTO vipfqdn VALUES (?,?)',(fqdn,ip))

conn.commit()
conn.close()
