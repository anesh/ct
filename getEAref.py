import requests
import json
requests.packages.urllib3.disable_warnings()


url = "https://ibgrid/wapi/v2.7/extensibleattributedef?_return_as_object=1"
headers = {'content-type': "application/json"}
response = requests.request("GET", url, auth=('', ''), headers=headers,verify=False)
print response.text

