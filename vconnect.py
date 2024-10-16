import json
import getpass
from pyVim.connect import SmartConnect
import ssl

with open("vcenter-conf.json") as f:
    config = json.load(f)["vcenter"]

passw = getpass.getpass()
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE

si=SmartConnect(host=config["vcenterhost"], user=config["vcenteradmin"], pwd=passw, sslContext=s)

#Test config 