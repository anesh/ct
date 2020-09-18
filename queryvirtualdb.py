import sqlite3

conn = sqlite3.connect('vipstatus.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM vipstatus INNER JOIN vipfqdn ON vipstatus.ip = vipfqdn.ip'):
	print row

