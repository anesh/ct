from netmiko import ConnectHandler
import argparse
import yaml
from ciscoconfparse import CiscoConfParse

parser = argparse.ArgumentParser(description='''Cisco Demo''')
required = parser.add_argument_group('required arguments')
required.add_argument('-c', '--credfile', action='store', dest='credfile', help='AD username',required=True)
args = parser.parse_args()
credfile = args.credfile
f = open(credfile,'r')
cred = yaml.load(f)



net_connect = ConnectHandler(device_type='cisco_ios', host='42.200.150.240', username=cred['ctc']['ctcusername'], password=cred['ctc']['ctcpassword'])
preoutput = net_connect.send_command("show run | i logging")
print "PRE-CHECK...\n"
print preoutput
base=preoutput.splitlines()
config_commands = ['logging buffered 53000']
net_connect.send_config_set(config_commands)

postoutput = net_connect.send_command("show run | inc logging")
print "POST-CHECK...\n"
print postoutput
change=postoutput.splitlines()
print "DIFFERENCE..\n"

parse = CiscoConfParse(base)
print '\n'.join(parse.sync_diff(change, ''))