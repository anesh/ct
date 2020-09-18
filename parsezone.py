import dns.zone
import dns.resolver
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *
import difflib
import sys
import argparse

parser = argparse.ArgumentParser(description='''Infoblox Migration Validation tool to provide diff
					     output between DNS resolutions among nameservers
					''')

#parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument('-n', '--nameservers', action='store', dest='nameservers',required=True)
required.add_argument('-d', '--domain', action='store', dest='domain',required=True)
required.add_argument('-z', '--zonefile', action='store', dest='zonefile',required=True)
required.add_argument('-b', '--basenameserver', action='store', dest='basenameserver',required=True)

args = parser.parse_args()
nameserversfile = args.nameservers
nameofdomain = args.domain
nameofzonefile = args.zonefile
basenameserverfile = args.basenameserver


domain = nameofdomain
zone_file = nameofzonefile

f1 = open(nameserversfile,'r').read().splitlines()
nameservers = f1

for nameserver in nameservers:
	print nameserver
	f2=open(nameserver,'w')
	intresolver = dns.resolver.Resolver()
	intresolver.nameservers = [nameserver]
	intresolver.timeout = 2
	intresolver.lifetime = 2

	try:
    		zone = dns.zone.from_file(zone_file, domain)
    		for name, node in zone.nodes.items():
        		rdatasets = node.rdatasets
        		for rdataset in rdatasets:
            			for rdata in rdataset:
					try:
                				if rdataset.rdtype == SOA:
		    					print rdataset.rdtype
                				if rdataset.rdtype == MX:
		    					print str(name),rdataset.rdtype
                				if rdataset.rdtype == NS:
		    					print str(name)
                				if rdataset.rdtype == CNAME:
		   	
		    					intanswers= intresolver.query(name,'CNAME')
                    					print intanswers.rrset
							f2.write(str(intanswers.rrset))
							f2.write("\n")
                				if rdataset.rdtype == A:
		    					intanswers= intresolver.query(name,'A')
		    					print intanswers.rrset
							f2.write(str(intanswers.rrset))
							f2.write("\n")
					except DNSException, e:
		    				print e.__class__, e




	
	except DNSException, e:
   		 print e.__class__, e

	f2.close()

base = basenameserverfile

for nameserver in nameservers:
	f3 = open(nameserver+"_"+base+".html",'w')
	text1 = open(base).readlines()
	text2 = open(nameserver).readlines()
	diff = difflib.HtmlDiff().make_file(text1,text2,base,nameserver)
	f3.write(diff)
	f3.close()

