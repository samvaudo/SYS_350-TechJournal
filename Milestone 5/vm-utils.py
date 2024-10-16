import json
import getpass
from pyVim.connect import SmartConnect, vim
import ssl


def pyVimConnect(jsonfile):
    with open(jsonfile) as f:
        config = json.load(f)['vcenter'][0]

    passw = getpass.getpass()
    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s.verify_mode=ssl.CERT_NONE


    si=SmartConnect(host=config['vcenterhost'], user=config['vcenteradmin'], pwd=passw, sslContext=s)
    return si

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

si = pyVimConnect("vcenter-conf.json")
vms = searchvms(si)

si.RetrieveContent()