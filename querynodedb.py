import sqlite3

f = open('node.txt','r')
nodelist = f.read().splitlines()
conn = sqlite3.connect('vipmap.db')
c = conn.cursor()


for node in nodelist:
	search = '%'+node+'%'
	t= (search,)
	print t
	#for row in c.execute('SELECT * FROM vipobjs INNER JOIN poolobjs ON vipobjs.poolname = poolobjs.poolvirtual WHERE poolmember LIKE ?',t):
	for row in c.execute('SELECT * FROM policyobjs INNER JOIN virtualpolicyobjs ON policyobjs.policyname = virtualpolicyobjs.vpolicy WHERE policypoolmember LIKE ?',t):	
        	print row

