import json
import getpass
from pyVim.connect import SmartConnect, vim
import ssl
import socket

#Requirement 1
with open("vcenter-conf.json") as f:
    config = json.load(f)['vcenter'][0]

passw = getpass.getpass()
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE


si=SmartConnect(host=config['vcenterhost'], user=config['vcenteradmin'], pwd=passw, sslContext=s)

#Requirement 2
print('Domain: '+config['vcenterhost'])
print('Username: '+config['vcenteradmin'])
print("Vcenter Server Info:")
print(si.content.about)
print("IP address")
print(socket.gethostbyname(socket.gethostname()))

#Requirement 3
def searchvms(siobject, name = "ALL"):
    allobj= {}
    objectstoreturn = []
    container = siobject.content.viewManager.CreateContainerView(siobject.content.rootFolder, [vim.VirtualMachine],True)
    for objects in container.view:
        allobj.update({objects.name: objects})
        objectstoreturn.append(objects)
    if name == "ALL":
        return objectstoreturn
    else:
        if name in allobj:
            return allobj[name]
        else:
            print("name not found")
            return None
        


#Requirement 4

vms = searchvms(si)
print("VM Raw Names and Normal Name")
for item in vms: #Printing all VMs and meta data
    print("Name: " + item.name)
    print("Status: " + item.guest.guestState)
    print("Number of CPUs: "+str(item.summary.config.numCpu))
    print("Memory (GB): " + str(item.summary.config.memorySizeMB/1024))
    print("IP Adress: " + str(item.guest.ipAddress))

