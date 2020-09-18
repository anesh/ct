from __future__ import print_function
import re
import requests
from orionsdk import SwisClient
requests.packages.urllib3.disable_warnings()

def main():
   npm_server = 'swwindsserver'
   username = ''
   password = ''


   swis = SwisClient(npm_server, username, password, verify=False)

   # Only need one of [DisplayName, Caption, NodeName]
   Orion_Nodes = {
      'DisplayName': "gw-dev-swtch-1.ns.ctc",
      'Description': "test",
      'NodeDescription': "test",
      'Location': "Lab",
      'UnManaged': False,
      'Allow64BitCounters': True,
      'ObjectSubType': "SNMP",
      'EngineID': 1,
      'IPAddress': "42.200.150.240",
      'SNMPVersion': '3',
      'SNMPV3Username': "###",
      'SNMPV3PrivMethod': "AES128",
      'SNMPV3PrivKeyIsPwd': True,
      'SNMPV3PrivKey': "###",
      'SNMPV3AuthKey': "###",
      'SNMPV3AuthMethod': "SHA1",
      'SNMPV3AuthKeyIsPwd': True
   }

   print("Add an SNMP v3 node:")
   print("Adding node {}... ".format(Orion_Nodes['IPAddress']), end="")
   results = swis.create('Orion.Nodes', **Orion_Nodes)
   print(results)
   
   nodeid = re.search(r'(\d+)$', results).group(0)
   
   # Assign an existing SNMPv3 credential set
   snmpresults = swis.query("SELECT Uri From Orion.NodeSettings WHERE NodeID=@id "
                           "AND SettingName='ROSNMPCredentialID'", id=nodeid)
   print(snmpresults)
   uri = snmpresults['results'][0]['Uri']
   swis.delete(uri)

   properties = {
        'NodeID': nodeid,
        'SettingName': 'ROSNMPCredentialID',
        'SettingValue': 'Cisco-SNMPv3'
   }

   results = swis.create('Orion.NodeSettings', **properties)
   
   #add pollers
   pollers_enabled = {
        'N.Status.ICMP.Native': True,
        'N.Status.SNMP.Native': False,
        'N.ResponseTime.ICMP.Native': True,
        'N.ResponseTime.SNMP.Native': False,
        'N.Details.SNMP.Generic': True,
        'N.Uptime.SNMP.Generic': True,
        'N.Cpu.SNMP.HrProcessorLoad': True,
        'N.Memory.SNMP.NetSnmpReal': True,
        'N.AssetInventory.Snmp.Generic': True,
        'N.Topology_Layer3.SNMP.ipNetToMedia': False,
        'N.Routing.SNMP.Ipv4CidrRoutingTable': False
    }

   pollers = []
   for k in pollers_enabled:
        pollers.append(
            {
                'PollerType': k,
                'NetObject': 'N:' + nodeid,
                'NetObjectType': 'N',
                'NetObjectID': nodeid,
                'Enabled': pollers_enabled[k]
            }
        )

   for poller in pollers:
        print("  Adding poller type: {} with status {}... ".format(poller['PollerType'], poller['Enabled']), end="")
        response = swis.create('Orion.Pollers', **poller)
        print("DONE!")

   '''
   #update custom properties
   customresults = swis.query("SELECT Uri FROM Orion.Nodes WHERE NodeID=@id",id=nodeid)
   print(customresults)
   uri = customresults['results'][0]['Uri']

   swis.update(uri + '/CustomProperties', Support_Team='Corp Network')
   obj = swis.read(uri + '/CustomProperties')
   print (obj)
   '''


if __name__ == '__main__':
   main()
