from ncclient import manager
import xmltodict
from xml.dom import minidom

device={"address":"sandbox-iosxe-recomm-1.cisco.com",
        "port":830,
        "username":"developer",
        "password":"C1sco12345"
        }
nc_filter = open("c:/Users/Hudso/Modeldrive/Md_Netconf/filter.xml").read()

if __name__=='__main__':
    with manager.connect(host=device["address"], port=device["port"],
                         username=device["username"],
                         password=device["password"],
                         hostkey_verify=False) as c_device:
        print(" ")
        
        print("Device connected : {}.\n".format(c_device.connected))
        
        print("All capabilities of the connected NetConf session stored in capabilities.txt file\n")

        with open("c:/Users/Hudso/Modeldrive/Md_Netconf/capabilities.txt","w") as file:
            for capability in c_device.server_capabilities:
                file.write(str(capability))

        netconf_reply=c_device.get_config("running")

        print("\nRunning configuration is in {} format".format(type(netconf_reply)))

        print("\nConfiguration stored in running.txt file\n")

        with open("c:/Users/Hudso/Modeldrive/Md_Netconf/running.txt","w") as file:
            file.write(str(netconf_reply))

        netconf_reply_dict=xmltodict.parse(netconf_reply.xml)

        print("\nRunning configuration now in {} format".format(type(netconf_reply_dict)))

        print(" ")

        print("Configuration converted to a dictionary and stored in running_dict.txt file\n")

        with open("c:/Users/Hudso/Modeldrive/Md_Netconf/running_dict.txt","w") as file:
            file.write(str(netconf_reply_dict))

        print("Let's start working with only targeted configuration by apply filter to running configuration\n")


        running_filtered = c_device.get_config("running",nc_filter)

        print(type(running_filtered))
        
        print("\n")

        running_filtered_xml = minidom.parseString(running_filtered.xml)

        print(running_filtered_xml.toprettyxml(indent = "  "))

        running_filtered_dict = xmltodict.parse(running_filtered.xml)


        intf = running_filtered_dict["rpc-reply"]["data"]["interfaces"]["interface"]

        print("")
        print("  Name: {}".format(intf["name"]["#text"]))
        print("  Description: {}".format(intf["description"]))
        print("  Type: {}".format(intf["type"]["#text"]))
        print("  Enabled: {}".format(intf["enabled"]))

        print(" ")

        print("configuring via NETCONF")

        temp = open("c:/Users/Hudso/Modeldrive/Md_Netconf/template.xml").read()

        adding_config = temp.format(int_name="Loopback22",
                                              int_desc="Configured by NETCONF",
                                              ip_address="10.255.255.1",
                                              subnet_mask="255.255.255.0"
                                              )
        print(adding_config)

        print(" ")

        print(c_device.connected)

        nc_reply = c_device.edit_config(target="running", config=adding_config)

        print(" ")

        print("Configuration changes successfully made ? : {} \n".format(nc_reply.ok))

        print(" ")

        print("Now deleting that created loopback via NetConf")

        delete = open("c:/Users/Hudso/Modeldrive/Md_Netconf/del_template.xml").read()

        del_var = delete.format(int_name="Loopback22")

        delete_reply = c_device.edit_config(target="running",config=del_var)

        print("Specified configuration successfully deleted ? : {} \n".format(delete_reply.ok))

        
