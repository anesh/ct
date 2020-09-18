
import sqlite3


'''
conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM vipobjs INNER JOIN poolobjs ON vipobjs.poolname = poolobjs.poolvirtual '):
        print row

conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM policyobjs'):
        print row


conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM virtualpolicyobjs'):
        print row
'''


conn = sqlite3.connect('vipmap.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM policyobjs INNER JOIN virtualpolicyobjs ON policyobjs.policyname = virtualpolicyobjs.vpolicy '):
        print row

