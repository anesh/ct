import requests
from orionsdk import SwisClient
requests.packages.urllib3.disable_warnings()
import argparse
import yaml

example_text = '''


   The file that you pass as argumnet to "c" must be in YAML format, see below for an example
        ctb:
            ctbusername: aneshctb
            ctbpassword: passwordctb
        ctc:
            ctcusername: aneshctc
            ctcpassword: passwordctc


 !!!Example to generate CTFS inventory and send output to a file names ctfs.txt:

 python swinventory.py -c account.txt -s CTFS >> ctfs.txt

 !!!Example to generate CTC inventory and send output to a file name ctc.txt

 python swinventory.py -c account.txt -s CTC >> ctc.txt

!!!Example to generate CTFS inventory for Cisco NX-OS devices

python swinventory.py -c account.txt -s CTFS -v Cisco -t 'Cisco NX-OS%' 

!!!Example to generate CTFS inventory for Cisco IOS devices

python swinventory.py -c account.txt -s CTFS -v Cisco -t 'Cisco IOS%'


'''


parser = argparse.ArgumentParser(description='''SolarWinds Inventory Generation tool
					''',epilog=example_text,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

required = parser.add_argument_group('required arguments')
required.add_argument('-c', '--credfile', action='store', dest='credfile', help='AD username',required=True)
required.add_argument('-s', '--sbu', action='store', dest='business', help='AD password',required=True)
required.add_argument('-v', '--vendor', action='store', dest='vendor', help='Cisco/F5/Infoblox',required=True)

parser.add_argument('-t', '--type', action='store', dest='machinetype', help='CiscoIOS/NXOS')

args = parser.parse_args()
credfile = args.credfile
business = args.business
vendor = args.vendor
machinetype = args.machinetype 
f = open(credfile,'r')
cred = yaml.load(f)
username = cred['ctb']['ctbusername']
password = cred['ctb']['ctbpassword'] 
def main():
    npm_server = ''

    swis = SwisClient(npm_server, username, password)

    sbu=business
    if machinetype:
	results = swis.query("SELECT Caption AS NodeName, IPAddress FROM Orion.Nodes WHERE Nodes.CustomProperties.SBU = @sbu and Vendor = @vendor and NodeDescription like @machinetype",sbu=sbu,vendor=vendor,machinetype=machinetype)
    else:
	results = swis.query("SELECT Caption AS NodeName, IPAddress FROM Orion.Nodes WHERE Nodes.CustomProperties.SBU = @sbu and Vendor = @vendor",sbu=sbu,vendor=vendor)
    for result in results['results']:
	print result['IPAddress'], result['NodeName']
if __name__ == '__main__':
    main()

