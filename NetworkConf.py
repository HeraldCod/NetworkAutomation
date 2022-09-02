from ncclient import manager
import xmltodict

router = {'address':'sandbox-iosxr-1.cisco.com',
'netconf_port':830 ,
'username':'admin',
'password':'C1sco12345'}               # Dictionary with the login information of the targeting router

router_manager=manager.connect(host = router["address"],
port = router["netconf_port"],
username=router["username"],
password=router["password"],
hostkey_verify=False)                   # Connecting the router via ncclient manager 

print(type(router_manager))

print(router_manager.connected)         # Check for connection

f= open('Capabilities.txt','w')

for capability in router_manager.server_capabilities:
    f.write(capability)                                  # Writing all netconf capabilities to a file
f.close()

Running_config=router_manager.get_config("running")
g=open('Running.txt','w')
g.write(str(Running_config))                            # Copying running configuration to a file in xml format
g.close()

print(type(Running_config))

Running_config_dict=xmltodict.parse(Running_config.xml)    # Converting Xml configuration to python dictionary
h=open('configDict.txt','w')
h.write(str(Running_config_dict))                          # Writing configuration to a file in dictionary format
h.close()
