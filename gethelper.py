import os
import re
from ciscoconfparse import CiscoConfParse
import paramiko
from ansible.module_utils.basic import AnsibleModule


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('', username='', password='',timeout=5,allow_agent=False,look_for_keys=False)
stdin,stdout,stderr = ssh.exec_command('show running-config ')
config = stdout.readlines()

parse = CiscoConfParse(config)
found_objs= parse.find_objects_w_child(parentspec=r"^interface", childspec=r"ip dhcp relay address")
for section in found_objs:
	print section.text


