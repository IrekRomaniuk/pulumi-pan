"""An Azure Python Pulumi program"""

import pulumi,json
import pulumi_azure as azure
import json, requests

env = pulumi.get_stack()
project = pulumi.get_project()
config = pulumi.Config()
data = config.require_object('data')
rg_name = data['rg_name']+'-'
password = config.require('password')

# Create an Azure Resource Group
resource_group = azure.core.ResourceGroup(rg_name)
'''
with open(data['dp-file']) as f:
    content = json.load(f)
'''    
content = requests.get(data['gitUrl']+'/template.json')
if (content.status_code != 200):
    print ('Can NOT get the template file')
    exit()
dp = content.json()    
# print (dp["parameters"])
# print (password)
# print (json.dumps(dp,separators=(',', ':')))
# Create an ARM template deployment
armDeployment = azure.core.TemplateDeployment(pulumi.get_project(), 
    resource_group_name= resource_group.name,
    template_body= json.dumps(dp,separators=(',', ':')), #JSON.stringify
    parameters= {
        "virtualNetworkName": "fwnet",
        "adminUsername": "azureuser",
        "adminPasswordOrKey": password,
        "publicIPAddressName": 'fwpip',
        "srcIPInboundNSG":"108.12.234.245",
        # "imageVersion":"9.1.2",
        "location": resource_group.location
    },
    deployment_mode= "Incremental",
)

# Export the connection string for the storage account
# pulumi.export('connection_string', account.primary_connection_string)
