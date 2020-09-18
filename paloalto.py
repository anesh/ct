import requests
import argparse
from bs4 import BeautifulSoup
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_UNDERLINE
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


#argument parser
parser = argparse.ArgumentParser(description='Build Book Automation Script')
parser.add_argument('-c','--client', help='Input Client Name',required=True)
args = parser.parse_args()

print ("Provide Client Name: %s" % args.client )


#rest api call for api key
r = requests.get('https://192.168.5.250/api/?type=keygen&user=username=password',verify=False)
markup = r.text
soup = BeautifulSoup(markup, "xml")
key = soup.find_all('key')
api=key[0].get_text()
#rest call for system information
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><system><info></info></system></show>&key='+api,verify=False)
tags =r.text
infomarkup = BeautifulSoup(tags, "xml")

#rest call for hardware interface information
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><interface>hardware</interface></show>&key='+api,verify=False)
hwinttags=r.text
hwintmarkup=BeautifulSoup(hwinttags, "xml")

#rest call for logical interface information
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><interface>logical</interface></show>&key='+api,verify=False)
loginttags=r.text
logintmarkup=BeautifulSoup(loginttags, "xml")

#rest call for routing table
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><routing><route></route></routing></show>&key='+api,verify=False)
routetags=r.text
routemarkup=BeautifulSoup(routetags, "xml")

#rest call for finding admins
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><admins><all></all></admins></show>&key='+api,verify=False)
admintags=r.text
adminmarkup=BeautifulSoup(admintags, "xml")

#rest call for vpn tunnels
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><vpn><flow></flow></vpn></show>&key='+api,verify=False)
vpntags=r.text
vpnmarkup=BeautifulSoup(vpntags, "xml")

#rest call for HA state
r = requests.get('https://192.168.5.250/api/?type=op&cmd=<show><high-availability><all></all></high-availability></show>&key='+api,verify=False)
hatags=r.text
hamarkup=BeautifulSoup(hatags, "xml")


#parsing xml for system information
hostname=infomarkup.find("hostname")
hostip=infomarkup.find("ip-address")
defaultgw=infomarkup.find("default-gateway")
model=infomarkup.find("model")
serial=infomarkup.find("serial")
swversion=infomarkup.find("sw-version")
family=infomarkup.find("family")

globalprotect=infomarkup.find("global-protect-client-package-version")
appversion=infomarkup.find("app-version")
avversion=infomarkup.find("av-version")
threatversion=infomarkup.find("threat-version")
wildfireversion=infomarkup.find("wf-private-version")



interfaces=[]
for interface in hwintmarkup.find_all("entry"):
	interfaced={'name':str(interface.find('name').get_text()),
	            'duplex':str(interface.duplex.get_text()),
				'state':str(interface.state.get_text()),
				'mac':str(interface.mac.get_text()),
				}
	interfaces.append(interfaced)

loginterfaces=[]
for logint in logintmarkup.find_all("entry"):
	logintd={'name':str(logint.find('name').get_text()),
			 'zone':str(logint.zone.get_text()),
			 'ip':str(logint.ip.get_text())
			 }
	loginterfaces.append(logintd)
	
routes=[]
for route in routemarkup.find_all("entry"):
	routed={'destination':str(route.destination.get_text()),
			'nexthop':str(route.nexthop.get_text()),
			'metric':str(route.metric.get_text()),
			'interface':str(route.interface.get_text())
			}
	routes.append(routed)
	
admins=[]
for admin in adminmarkup.find_all("entry"):
	val=admin.attrs
	admins.append(val['name'])
	
vpntunnel=[]
for vpntunnels in vpnmarkup.find_all("entry"):
	vpntunneld={'name':str( vpntunnels.find("name").get_text()),
				'state':str(vpntunnels.state.get_text()),
				'interface':str(vpntunnels.find("inner-if").get_text()),
				'localip':str(vpntunnels.localip.get_text()),
				'peerip':str(vpntunnels.peerip.get_text()),
				'localid':str(vpntunnels.find("proxy-id").lip.get_text()),
				'peerid':str(vpntunnels.find("proxy-id").rip.get_text())
				}
	vpntunnel.append(vpntunneld)
	
ha=[]
ha.append(str(hamarkup.find("local-info").find("ha1-ipaddr").get_text()))
ha.append(str(hamarkup.find("local-info").priority.get_text()))
ha.append(str(hamarkup.find("local-info").find("ha2-macaddr").get_text()))
ha.append(str(hamarkup.find("local-info").find("preemptive").get_text()))
ha.append(str(hamarkup.find("local-info").find("state").get_text()))
ha.append(str(hamarkup.find("local-info").find("mode").get_text()))

ha.append(str(hamarkup.find("peer-info").find("ha1-ipaddr").get_text()))
ha.append(str(hamarkup.find("peer-info").priority.get_text()))
ha.append(str(hamarkup.find("peer-info").find("ha2-macaddr").get_text()))
ha.append(str(hamarkup.find("peer-info").find("preemptive").get_text()))
ha.append(str(hamarkup.find("peer-info").find("state").get_text()))

ha.append(str(hamarkup.find("link-monitoring").find("enabled").get_text()))
ha.append(str(hamarkup.find("path-monitoring").find("enabled").get_text()))

hakeys=["LocalHa1","LocalPriority","localHA2Mac","LocalPremptive","LocalState","LocalMode",
"PeerHa1","PeerPriority","PeerHa2MAC","PeerPremptive","PeerState","LinkMonitor","PathMonitor"]



#build dictionary for system information
systeminfo={"hostname":str(hostname.get_text()),"ipaddress":str(hostip.get_text()),"default-gateway":str(defaultgw.get_text()),
"model":str(model.get_text()),"serial":str(serial.get_text()),"swversion":str(swversion.get_text()),"family":str(family.get_text())}

#build dictionary for license information
licinfo={"globalprotect":str(globalprotect.get_text()),"appversion":str(appversion.get_text()),"avversion":str(avversion.get_text()),
