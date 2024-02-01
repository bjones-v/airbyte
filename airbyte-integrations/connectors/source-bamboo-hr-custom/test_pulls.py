import requests
import xmltodict
# import xml.etree.ElementTree as ET
import json


url = "https://api.bamboohr.com/api/gateway.php/printerlogic/v1/employees/changed/tables/customJobRequisition?since=2024-02-01T00%3A00%3A00%2B0000"

# url = "https://api.bamboohr.com/api/gateway.php/printerlogic/v1/employees/directory"


headers = {"authorization": "Basic NGUzMjYyM2Y3NTlmYzQ5ZjRhNjdhNDg2YWYzOGY2YjA4NzczOTcxMTp4"}

response = requests.get(url, headers=headers)

# response_dict = xmltodict.parse(response.text)

# response_json = json.dumps(response_dict)

# output = json.dumps(xmltodict.parse(response.text))
output = response.text

print(output)



