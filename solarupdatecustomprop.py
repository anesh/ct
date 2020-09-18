import requests
from orionsdk import SwisClient


def main():
    npm_server = ''
    username = ''
    password = ''

    swis = SwisClient(npm_server, username, password)
    results = swis.query("SELECT Uri FROM Orion.Nodes WHERE NodeID=@id",id=870)  
    
    print results
    uri = results['results'][0]['Uri']

    swis.update(uri + '/CustomProperties', Support_Team='Corp Network')
    obj = swis.read(uri + '/CustomProperties')
    print (obj)

requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
