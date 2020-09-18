import requests
import shutil
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

r = requests.get('https://solarwindserver:17778/SolarWinds/InformationService/v3/Json/Query?query=SELECT NodeID from Orion.Nodes WHERE Vendor = "Cisco"', auth=('', ''),verify=False)
print(r.text)
print r.status_code
