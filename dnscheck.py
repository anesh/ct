import dns.resolver

f1 = open('fqdns.txt','r')

fqdns = f1.read().splitlines() 
#print fqdns
intresolver = dns.resolver.Resolver()
intresolver.nameservers = ['10.255.255.253']
intresolver.timeout = 2
intresolver.lifetime = 2

extresolver = dns.resolver.Resolver()
extresolver.nameservers = ['199.202.145.0']
extresolver.timeout = 2
extresolver.lifetime = 2


#rlist=['A','CNAME']
#rlist = ['CNAME']
rlist = ['A']

for fqdn in fqdns:
	for r in rlist:
		try:
			intanswers= intresolver.query(fqdn,r)
			print intanswers.rrset
		except:
			pass
'''	
	for r in rlist:
		try:
                	extanswers = extresolver.query(fqdn,r)
			print extanswers.rrset,"external"
        	except:
                	pass
'''	



