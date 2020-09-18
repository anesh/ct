import requests
from orionsdk import SwisClient
requests.packages.urllib3.disable_warnings()

def main():
    npm_server = 'swwindserver'
    username = ''
    password = ''

    swis = SwisClient(npm_server, username, password)

    '''
    batchresults = swis.query("SELECT Result, ResultDescription, ErrorMessage, BatchID FROM Orion.DiscoveryLogs WHERE ProfileID=@id", id="62")
    batchid= batchresults['results'][0]['BatchID'] 
    nodeidresults = swis.query("SELECT DisplayName,NetObjectID FROM Orion.DiscoveryLogItems WHERE BatchID=@id", id=batchid)
    netobjectid = nodeidresults['results'][0]['NetObjectID']
    nodeid= netobjectid.split(':')[1]
    print(nodeid)
    customresults = swis.query("SELECT Uri FROM Orion.Nodes WHERE NodeID=@id",id=nodeid)
    print(customresults)
    '''
    '''
    nodeid=890
    pollerdata = swis.query("SELECT PollerType FROM Orion.Pollers WHERE NetObjectID=@nodeid", nodeid=nodeid)
    for row in pollerdata['results']:
    	print row
    '''
    #ip="8.8.8.8"
    #results = swis.query("SELECT Caption AS NodeName, IPAddress FROM Orion.Nodes WHERE IPAddress =@ip ",ip=ip)
    results = swis.query("SELECT Caption AS NodeName, IPAddress,MachineType,IOSImage,NodeDescription FROM Orion.Nodes WHERE Nodes.CustomProperties.SBU = 'CTFS'")
    
    for result in results['results']:
	print result['IPAddress'],result['NodeDescription']
	#print result['IOSImage'],result['NodeName']
	#print result['MachineType']
	#print result['IPAddress'], result['NodeName']
if __name__ == '__main__':
    main()

